"""Tests for the models of the ``document_library`` app."""
from mock import Mock

from django.test import TestCase

from ..models import Document, DocumentPlugin
from .factories import (
    AttachmentFactory,
    DocumentFactory,
    DocumentCategoryFactory,
    DocumentCategoryTitleENFactory,
    DocumentTitleDEFactory,
    DocumentTitleENFactory,
)


class AttachmentTestCase(TestCase):
    """Tests for the ``Attachment`` model."""
    longMessage = True

    def test_model(self):
        obj = AttachmentFactory()
        self.assertTrue(obj.pk, msg=(
            'Should be able to instantiate and save the model.'))


class DocumentTestCase(TestCase):
    """Tests for the ``Document`` model."""
    longMessage = True

    def test_model(self):
        instance = DocumentFactory()
        self.assertTrue(instance.pk, msg=(
            'Should be able to instantiate and save the object.'))

    def test_get_filetype(self):
        title = DocumentTitleENFactory()
        instance = title.document
        result = instance.get_filetype()
        self.assertEqual(result, None, msg=(
            'Should return the translated filetype.'))

    def test_get_title(self):
        title = DocumentTitleENFactory()
        instance = title.document
        result = instance.get_title()
        self.assertEqual(result, 'A title', msg=(
            'Should return the translated title.'))


class DocumentCategoryTestCase(TestCase):
    """Tests for the ``DocumentCategory`` model."""
    longMessage = True

    def test_model(self):
        instance = DocumentCategoryFactory()
        self.assertTrue(instance.pk, msg=(
            'Should be able to instantiate and save the object.'))

    def test_get_title(self):
        title = DocumentCategoryTitleENFactory()
        instance = title.category
        result = instance.get_title()
        self.assertEqual(result, 'A title', msg=(
            'Should return the translated title.'))


class DocumentCategoryTitleTestCase(TestCase):
    """Tests for the ``DocumentCategoryTitle`` model."""
    longMessage = True

    def test_model(self):
        instance = DocumentCategoryTitleENFactory()
        self.assertTrue(instance.pk, msg=(
            'Should be able to instantiate and save the object.'))


class DocumentManagerTestCase(TestCase):
    """Tests for the ``DocumentManager`` model manager."""
    longMessage = True

    def setUp(self):
        self.en_title = DocumentTitleENFactory(is_published=False)
        self.de_title = DocumentTitleDEFactory(is_published=False)
        DocumentTitleENFactory(document=self.de_title.document)
        DocumentTitleDEFactory(document=self.en_title.document)

    def test_manager(self):
        """Testing if the ``DocumentManager`` retrieves the correct objects."""
        request = Mock(LANGUAGE_CODE='de')
        self.assertEqual(
            Document.objects.published(request).count(), 1, msg=(
                'In German, there should be one published document.'))

        request = Mock(LANGUAGE_CODE='en')
        self.assertEqual(
            Document.objects.published(request).count(), 1, msg=(
                'In English, there should be one published document.'))

        request = Mock(LANGUAGE_CODE=None)
        self.assertEqual(
            Document.objects.published(request).count(), 0, msg=(
                'If no language is set, there should be no published'
                ' documents.'))


class DocumentPluginTestCase(TestCase):
    """Tests for the ``DocumentPlugin`` model."""
    longMessage = True

    def test_model(self):
        instance = DocumentPlugin(document=DocumentFactory())
        instance.save()
        self.assertTrue(instance.pk, msg=(
            'Should be able to instantiate and save the object.'))


class DocumentTitleTestCase(TestCase):
    """Tests for the ``DocumentTitle`` model."""
    longMessage = True

    def test_model(self):
        instance = DocumentTitleENFactory()
        self.assertTrue(instance.pk, msg=(
            'Should be able to instantiate and save the object.'))
