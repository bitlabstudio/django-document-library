"""Tests for the models of the ``document_library`` app."""
from django.test import TestCase

from document_library.tests.factories import (
    DocumentFactory,
    DocumentCategoryFactory,
    DocumentCategoryTitleENFactory,
    DocumentTitleENFactory,
)


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


class DocumentTitleTestCase(TestCase):
    """Tests for the ``DocumentTitle`` model."""
    longMessage = True

    def test_model(self):
        instance = DocumentTitleENFactory()
        self.assertTrue(instance.pk, msg=(
            'Should be able to instantiate and save the object.'))
