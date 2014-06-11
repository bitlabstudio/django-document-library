# -*- coding: utf-8 -*-
"""Tests for the models of the ``document_library`` app."""
from __future__ import unicode_literals

from mock import Mock

from django.test import TestCase

from ..models import Document, DocumentPlugin
from .factories import (
    AttachmentFactory,
    DocumentFactory,
    DocumentCategoryFactory,
    FileFactory,
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
        instance = DocumentFactory()
        self.assertEqual(instance.get_filetype(), None, msg=(
            'Should return the translated filetype.'))

        instance.filer_file = FileFactory()
        self.assertEqual(instance.get_filetype(), '', msg=(
            'Should return the translated filetype.'))


class DocumentCategoryTestCase(TestCase):
    """Tests for the ``DocumentCategory`` model."""
    longMessage = True

    def test_model(self):
        instance = DocumentCategoryFactory()
        self.assertTrue(instance.pk, msg=(
            'Should be able to instantiate and save the object.'))

    def test_get_title(self):
        instance = DocumentFactory()
        result = instance.get_title()
        self.assertEqual(result, instance.title, msg=(
            'Should return the translated title.'))


class DocumentManagerTestCase(TestCase):
    """Tests for the ``DocumentManager`` model manager."""
    longMessage = True

    def setUp(self):
        self.en_doc = DocumentFactory(
            category=DocumentCategoryFactory(is_published=True),
            language_code='en', is_published=False)
        self.de_doc = DocumentFactory(
            category=DocumentCategoryFactory(is_published=True),
            language_code='de', is_published=False)
        self.de_doc_no_public_cat = DocumentFactory(
            category=DocumentCategoryFactory(is_published=False),
            language_code='de', is_published=False)
        new_doc = self.de_doc.translate('en')
        new_doc.is_published = True
        new_doc.save()
        new_doc = self.en_doc.translate('de')
        new_doc.is_published = True
        new_doc.save()
        new_doc = self.de_doc_no_public_cat.translate('en')
        new_doc.is_published = True
        new_doc.save()

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
