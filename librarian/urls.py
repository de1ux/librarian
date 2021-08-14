from django.contrib import admin
from django.urls import path

from librarian.api.views import document_views, config_views

urlpatterns = [
    path("admin/", admin.site.urls),

    # config endpoints
    path("api/config/", config_views.config_create, name='setup-data'),
    path("api/config/read", config_views.config_get, name='get-data'),

    # search endpoints
    path("api/documents/search", document_views.document_search, name='document-search'),
    path("api/documents/text/search", document_views.DocumentTextSearchView.as_view(), name='document-text-search')

    # document endpoints
    path("api/documents/", document_views.DocumentListView.as_view()),
    path("api/documents/<str:filename>", document_views.document_create, name='document-create'),
    path("api/documents/<int:id>/details", document_views.DocumentView.as_view()),
    path("api/documents/<int:id>/data", document_views.DocumentDataView.as_view()),

]
