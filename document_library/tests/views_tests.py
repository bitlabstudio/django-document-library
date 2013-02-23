"""Tests for the views of the ``document_library`` app."""
from django.test import TestCase, RequestFactory

from .factories import DocumentTitleENFactory
from document_library.views import DocumentDetailView, DocumentListView


class DocumentListViewTestCase(TestCase):
    """Tests for the ``DocumentListView`` view."""
    def test_view(self):
        req = RequestFactory().get('/')
        resp = DocumentListView.as_view()(req)
        self.assertEqual(resp.status_code, 200)


class DocumentDetailViewTestCase(TestCase):
    """Tests for the ``DocumentDetailView`` view."""
    def test_view(self):
        doc_title = DocumentTitleENFactory()
        req = RequestFactory().get('/')
        resp = DocumentDetailView.as_view()(req, pk=doc_title.pk)
        self.assertEqual(resp.status_code, 200)
