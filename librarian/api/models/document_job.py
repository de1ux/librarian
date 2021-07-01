import logging
import os
import subprocess
import tempfile
from datetime import datetime

from django.conf import settings
from django.db import models
from django.utils import timezone

from librarian import annotate
from librarian.api.models import DocumentStatus, DocumentPageImage
from librarian.utils.attrs import setattrs
from librarian.utils.enum import BaseEnum

logger = logging.getLogger(__name__)


class DocumentJobJobs(BaseEnum):
    persist = "PERSIST"
    translate_pdf_to_images = "TRANSLATE_TO_IMAGES"
    annotate = "ANNOTATE"


class DocumentJob(models.Model):
    document = models.ForeignKey('Document', on_delete=models.CASCADE)
    job = models.TextField(choices=DocumentJobJobs.choices())

    current_status = models.TextField(choices=DocumentStatus.choices())
    desired_status = models.TextField(choices=DocumentStatus.choices())

    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True)

    successful = models.BooleanField(null=True)
    failed_reason = models.TextField(null=True)

    def run(self):
        dc = self.document
        dc.status = self.current_status
        dc.save()

        successful = False
        failed_reason = None

        if self.job == DocumentJobJobs.persist:
            try:
                if settings.STORAGE_MODE == "local":
                    # TODO - no need to open / write, just move from temp to filestore path
                    with open(settings.LOCAL_STORAGE_PATH + "/" + dc.filename, mode="wb") as local_f, \
                            open(dc.temp_path, "rb") as tmp_f:
                        local_f.write(bytearray(tmp_f.read()))
                elif settings.STORAGE_MODE == "nfs":
                    import libnfs
                    # read temp file into nfs
                    nfs = libnfs.NFS(settings.NFS_PATH)
                    nfs_f = nfs.open("/" + dc.filename, mode="wb")
                    with open(dc.temp_path, "rb") as tmp_f:
                        nfs_f.write(bytearray(tmp_f.read()))
                    nfs_f.close()
                else:
                    raise Exception(f"Storage mode {settings.STORAGE_MODE} not recognized, quitting")

                # cleanup temp file
                os.remove(dc.temp_path)

                setattrs(
                    dc,
                    temp_path=None,
                    status=self.desired_status,
                    filestore_path=dc.filename,
                )
                dc.save()

                # TODO - this might not be the best place to kick off next transition
                dc.translate_pdf_to_images()
            except Exception as e:
                successful = False
                failed_reason = str(e)
                logger.exception(e)
            finally:
                setattrs(
                    self,
                    completed_at=timezone.now(),
                    successful=successful,
                    failed_reason=failed_reason,
                )

                self.save()

        if self.job == DocumentJobJobs.translate_pdf_to_images:
            try:
                b = dc.get_bytes_from_filestore()

                d = tempfile.mkdtemp()
                with tempfile.NamedTemporaryFile() as f:
                    f.write(b)

                    cmd = f"convert -density 150 {f.name} -quality 90 {d}/output.png"

                    start_time = datetime.now()
                    logger.debug(f"Starting conversion...: \n{cmd}")

                    subprocess.call(cmd.split(" "))

                    duration = (datetime.now() - start_time).total_seconds()
                    logger.debug(
                        f"Starting conversion...done in {duration}s: \n{cmd}"
                    )

                # list images from pdf split
                for filename in os.listdir(d):
                    page_number = 0

                    if filename != "output.png":
                        # take "output-5.png" and split to "5.png"
                        _, filename_parts = filename.split("-")
                        # split "5.png" to 5
                        page_number, _ = filename_parts.split(".")

                    DocumentPageImage.objects.create(document=dc, temp_path=f"{d}/{filename}",
                                                     page_number=int(page_number))

                dc.status = self.desired_status
                dc.save()
                dc.annotate()

            except Exception as e:
                successful = False
                failed_reason = str(e)
                logger.exception(e)
            finally:
                setattrs(
                    self,
                    completed_at=timezone.now(),
                    successful=successful,
                    failed_reason=failed_reason,
                )

                self.save()

        if self.job == DocumentJobJobs.annotate:
            try:
                logger.debug(f"Annotating {dc.documentpageimage_set.count()} pages...")
                for page in dc.documentpageimage_set.all():
                    with open(page.temp_path, mode="r+b") as tmp_f:
                        text, metadata = annotate(tmp_f.read())
                        setattrs(page, text=text, metadata=metadata)
                        page.save()

                logger.debug(f"Annotating {dc.documentpageimage_set.count()} pages...done")

                logger.debug(f"Freeing up /tmp image files...")

                for page in dc.documentpageimage_set.all():
                    os.remove(page.temp_path)
                    page.temp_path = None
                    page.save()

                logger.debug(f"Freeing up /tmp image files...done")

                dc.status = self.desired_status
                dc.save()
            except Exception as e:
                successful = False
                failed_reason = str(e)
                logger.exception(e)
            finally:
                setattrs(
                    self,
                    completed_at=timezone.now(),
                    successful=successful,
                    failed_reason=failed_reason,
                )

                self.save()