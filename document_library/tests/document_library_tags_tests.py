"""Tests for the templatetags of the ``document_library`` app."""
from django.template import RequestContext
from django.test import TestCase, RequestFactory

from model_bakery import baker

from ..templatetags import document_library_tags


class GetFilesForDocumentTestCase(TestCase):
    """Tests for the ``get_files_for_document`` templatetag."""
    longMessage = True

    def setUp(self):
        self.user = baker.make('auth.User')
        self.doc = baker.make('document_library.Document')
        self.doc.set_current_language('en')
        self.doc.set_current_language('de')

    def test_tag(self):
        result = document_library_tags.get_files_for_document(self.doc)
        self.assertEqual(len(result), 0, msg=(
            'Shouldn\'t return any files.'))


class GetFrontpageDocumentsTestCase(TestCase):
    """Tests for the ``get_frontpage_documents`` templatetag."""
    longMessage = True

    def setUp(self):
        super(GetFrontpageDocumentsTestCase, self).setUp()
        # Two documents that should be on the front page
        self.doc = baker.make(
            'document_library.Document',
            is_published=True,
        )
        self.doc.is_on_front_page = True
        self.doc.is_published = True
        self.doc.save()
        self.doc.set_current_language('de')
        self.doc.is_published = True
        self.doc.save()

        # And one that should not be on the front page
        baker.make('document_library.Document')

    def test_tag(self):
        req = RequestFactory().get('/')
        req.LANGUAGE_CODE = 'en'
        context = RequestContext(req)
        result = document_library_tags.get_frontpage_documents(context)
        self.assertEqual(result.count(), 1, msg=(
            'It should only return one document.'))
        self.assertEqual(result[0], self.doc, msg=(
            'Should return the one english document that has'
            ' is_on_fron_page=True'))

        req.LANGUAGE_CODE = 'de'
        context = RequestContext(req)
        result = document_library_tags.get_frontpage_documents(context)
        self.assertEqual(result.count(), 1, msg=(
            'It should only return one document.'))
        self.assertEqual(result[0], self.doc, msg=(
            'Should return the one german document that has'
            ' is_on_fron_page=True'))


class GetLatestDocumentsTestCase(TestCase):
    """Tests for the ``get_latest_documents`` tamplatetag."""
    longMessage = True

    def test_tag(self):
        baker.make('document_library.Document', is_published=True)
        baker.make('document_library.Document', is_published=True)
        baker.make('document_library.Document', is_published=True)
        baker.make('document_library.Document', is_published=False)

        req = RequestFactory().get('/')
        req.LANGUAGE_CODE = 'en'
        context = RequestContext(req)
        result = document_library_tags.get_latest_documents(context)
        self.assertEqual(result.count(), 3, msg=(
            'Should return up to five published documents'))

        result = document_library_tags.get_latest_documents(context, count=2)
        self.assertEqual(result.count(), 2, msg=(
            'Should return the requested number of published documents'))
