"""URLs for the ``document_library`` app."""
from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns(
    '',
    url(r'(?P<year>\d+)/(?P<month>\d+)/$',
        views.DocumentMonthView.as_view(),
        name='document_library_month'),
    url(r'^$',
        views.DocumentListView.as_view(),
        name='document_library_list'),
    url(r'^(?P<pk>\d+)/$',
        views.DocumentDetailView.as_view(),
        name='document_library_detail'),
)
