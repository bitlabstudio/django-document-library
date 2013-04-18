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

from document_library.templatetags.document_library_tags import (
    get_files_for_document,
    get_frontpage_documents,
)
from document_library.tests.factories import (
    DocumentTitleDEFactory,
    DocumentTitleENFactory,
)


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
        self.doc_en = DocumentTitleENFactory(filer_file=self.image)
        self.doc_de = DocumentTitleDEFactory(
            document=self.doc_en.document, filer_file=self.image)

    def tearDown(self):
        super(GetFilesForDocumentTestCase, self).tearDown()
        os.remove(self.filename)
        for f in File.objects.all():
            f.delete()

    def test_tag(self):
        result = get_files_for_document(self.doc_en.document)
        self.assertEqual(len(result), 2, msg=(
            'Should return all available files for all languages for the given'
            ' document'))


class GetFrontpageDocumentsTestCase(TestCase):
    """Tests for the ``get_frontpage_documents`` templatetag."""
    longMessage = True

    def setUp(self):
        super(GetFrontpageDocumentsTestCase, self).setUp()
        # Two documents that should be on the front page
        DocumentTitleENFactory(document__is_on_front_page=True)
        DocumentTitleDEFactory(document__is_on_front_page=True)

        # And one that should not be on the front page
        DocumentTitleDEFactory()

    def test_tag(self):
        req = RequestFactory().get('/')
        context = RequestContext(req)
        result = get_frontpage_documents(context)
        self.assertEqual(result.count(), 2, msg=(
            'Should return the two documents that have is_on_fron_page=True'))
