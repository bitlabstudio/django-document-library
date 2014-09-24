"""Tests for the templatetags of the ``document_library`` app."""
import os

from django.conf import settings
from django.core.files import File as DjangoFile
from django.template import RequestContext
from django.test import TestCase, RequestFactory

from filer.models.filemodels import File
from filer.models.imagemodels import Image
from filer.tests.helpers import create_image

from django_libs.tests.factories import UserFactory

from document_library.templatetags import document_library_tags as tags
from document_library.tests.factories import DocumentFactory


class GetFilesForDocumentTestCase(TestCase):
    """Tests for the ``get_files_for_document`` templatetag."""
    longMessage = True

    def setUp(self):
        super(GetFilesForDocumentTestCase, self).setUp()
        self.user = UserFactory()
        self.img = create_image()
        self.image_name = 'test_file.jpg'
        self.filename = os.path.join(
            settings.MEDIA_ROOT, self.image_name)
        self.img.save(self.filename, 'JPEG')
        self.file_obj = DjangoFile(open(self.filename), name=self.image_name)
        self.image = Image.objects.create(
            owner=self.user, original_filename=self.image_name,
            file=self.file_obj)
        self.doc_en = DocumentFactory(
            documenttranslation__language_code='en',
            filer_file=self.image)
        self.doc_de = DocumentFactory(
            documenttranslation__language_code='en',
            filer_file=self.image)

    def tearDown(self):
        super(GetFilesForDocumentTestCase, self).tearDown()
        os.remove(self.filename)
        for f in File.objects.all():
            f.delete()

    def test_tag(self):
        result = tags.get_files_for_document(self.doc_en)
        self.assertEqual(len(result), 1, msg=(
            'Should return only the english file for the given document'))


class GetFrontpageDocumentsTestCase(TestCase):
    """Tests for the ``get_frontpage_documents`` templatetag."""
    longMessage = True

    def setUp(self):
        super(GetFrontpageDocumentsTestCase, self).setUp()
        # Two documents that should be on the front page
        self.en_doc = DocumentFactory(
            language_code='en', is_published=True, is_on_front_page=True)
        self.de_doc = self.en_doc.translate('de')
        self.de_doc.is_published = True
        self.de_doc.save()

        # And one that should not be on the front page
        DocumentFactory()

    def test_tag(self):
        req = RequestFactory().get('/')
        req.LANGUAGE_CODE = 'en'
        context = RequestContext(req)
        result = tags.get_frontpage_documents(context)
        self.assertEqual(result.count(), 1, msg=(
            'It should only return one document.'))
        self.assertEqual(result[0], self.en_doc, msg=(
            'Should return the one english document that has'
            ' is_on_fron_page=True'))

        req.LANGUAGE_CODE = 'de'
        context = RequestContext(req)
        result = tags.get_frontpage_documents(context)
        self.assertEqual(result.count(), 1, msg=(
            'It should only return one document.'))
        self.assertEqual(result[0], self.de_doc, msg=(
            'Should return the one german document that has'
            ' is_on_fron_page=True'))


class GetLatestDocumentsTestCase(TestCase):
    """Tests for the ``get_latest_documents`` tamplatetag."""
    longMessage = True

    def test_tag(self):
        DocumentFactory(language_code='en', is_published=True)
        DocumentFactory(language_code='en', is_published=True)
        DocumentFactory(language_code='en', is_published=True)
        DocumentFactory(language_code='en', is_published=False)

        req = RequestFactory().get('/')
        req.LANGUAGE_CODE = 'en'
        context = RequestContext(req)
        result = tags.get_latest_documents(context)
        self.assertEqual(result.count(), 3, msg=(
            'Should return up to five published documents'))

        result = tags.get_latest_documents(context, count=2)
        self.assertEqual(result.count(), 2, msg=(
            'Should return the requested number of published documents'))
