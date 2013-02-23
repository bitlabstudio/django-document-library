"""URLs for the ``document_library`` app."""
from django.conf.urls.defaults import patterns, url

from .views import (
    DocumentDetailView,
    DocumentListView,
)


urlpatterns = patterns(
    '',
    url(r'^$',
        DocumentListView.as_view(),
        name='document_library_list'),

    url(r'^(?P<pk>\d+)/$',
        DocumentDetailView.as_view(),
        name='document_library_detail'),
)
