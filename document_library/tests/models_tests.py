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
    def test_model(self):
        instance = DocumentFactory()
        self.assertTrue(instance.pk)


class DocumentCategoryTestCase(TestCase):
    """Tests for the ``DocumentCategory`` model."""
    def test_model(self):
        instance = DocumentCategoryFactory()
        self.assertTrue(instance.pk)


class DocumentCategoryTitleTestCase(TestCase):
    """Tests for the ``DocumentCategoryTitle`` model."""
    def test_model(self):
        instance = DocumentCategoryTitleENFactory()
        self.assertTrue(instance.pk)


class DocumentTitleTestCase(TestCase):
    """Tests for the ``DocumentTitle`` model."""
    def test_model(self):
        instance = DocumentTitleENFactory()
        self.assertTrue(instance.pk)
