import {JobModel} from "../models/Job";
import {DocumentModel} from "../models/Document";
import {ResourceModel} from "../models/Resource";
import {FolderModel} from "../models/Folder";

export class Api {
    getDocuments(): Promise<ResourceModel<DocumentModel>> {
        return fetch("http://localhost:8000/api/documents/").then(d => d.json());
    }

    refreshJob(jobId: number): Promise<JobModel> {
        return fetch(`http://0.0.0.0:8000/api/documents/${jobId}/details`).then(d => d.json());
    }

    createDocument(acceptedFiles: any) {
        return acceptedFiles.map((file: any) => fetch(`http://0.0.0.0:8000/api/documents/${file.name}`, {
            method: 'POST',
            body: file,
        }).then(d => d.json()));
    }

    saveConfig(data: any) {
        return fetch('http://0.0.0.0:8000/api/config/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data),
        }).then(res => res.json());
    }

    createFolder(folderName: string) {
        return fetch('http://0.0.0.0:8000/api/folders/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({name: folderName, documents: []}),

        });
    }

    getFolders(): Promise<ResourceModel<FolderModel>> {
        return fetch('http://0.0.0.0:8000/api/folders/').then(d => d.json());
    }
}
