"""Tests for the models of the ``document_library`` app."""
from django.test import TestCase

from document_library.tests.factories import (
    DocumentFactory,
    DocumentTitleENFactory,
)


class DocumentTestCase(TestCase):
    """Tests for the ``Document`` model."""
    def test_model(self):
        instance = DocumentFactory()
        self.assertTrue(instance.pk)


class DocumentTitleTestCase(TestCase):
    """Tests for the ``DocumentTitle`` model."""
    def test_model(self):
        instance = DocumentTitleENFactory()
        self.assertTrue(instance.pk)
