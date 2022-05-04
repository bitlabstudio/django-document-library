# -*- coding: utf-8 -*-
"""Tests for the models of the ``document_library`` app."""
from __future__ import unicode_literals

from mock import Mock

from django.test import TestCase

from model_bakery import baker

from .. import models


class AttachmentTestCase(TestCase):
    """Tests for the ``Attachment`` model."""
    longMessage = True

    def test_model(self):
        obj = baker.make('document_library.Attachment')
        self.assertTrue(obj.pk, msg=(
            'Should be able to instantiate and save the model.'))


class DocumentTestCase(TestCase):
    """Tests for the ``Document`` model."""
    longMessage = True

    def test_model(self):
        instance = baker.make('document_library.Document')
        self.assertTrue(instance.pk, msg=(
            'Should be able to instantiate and save the object.'))

    def test_get_filetype(self):
        self.de_doc = baker.make('document_library.Document')
        self.de_doc.set_current_language('de')
        self.de_doc.title = 'DE'
        self.de_doc.save()

        self.assertEqual(self.de_doc.get_filetype(), '', msg='Should return the filetype.')

        self.de_doc.filer_file = baker.make('filer.File')
        self.de_doc.filer_file.file.name = 'image.jpg'
        self.assertEqual(self.de_doc.get_filetype(), 'JPG', msg=('Should return the filetype.'))


class DocumentCategoryTestCase(TestCase):
    """Tests for the ``DocumentCategory`` model."""
    longMessage = True

    def test_model(self):
        instance = baker.make('document_library.DocumentCategory')
        self.assertTrue(instance.pk, msg=(
            'Should be able to instantiate and save the object.'))

    def test_get_title(self):
        instance = baker.make('document_library.DocumentCategory')
        result = instance.get_title()
        self.assertTrue(result, msg=('Should return the translated title.'))


class DocumentManagerTestCase(TestCase):
    """Tests for the ``DocumentManager`` model manager."""
    longMessage = True

    def setUp(self):
        de_cat = baker.make('document_library.DocumentCategory', is_published=True)
        self.de_doc = baker.make('document_library.Document')
        self.de_doc.set_current_language('de')
        self.de_doc.category = de_cat
        self.de_doc.is_published = True
        self.de_doc.title = 'DE'
        self.de_doc.save()

        en_cat = baker.make('document_library.DocumentCategory', is_published=True)
        self.en_doc = baker.make('document_library.Document')
        self.en_doc.set_current_language('en')
        self.en_doc.category = en_cat
        self.en_doc.is_published = True
        self.en_doc.title = 'EN'
        self.en_doc.save()

        nonpub_cat = baker.make(
            'document_library.DocumentCategory',
            is_published=False
        )
        self.de_doc_no_public_cat = baker.make('document_library.Document')
        self.de_doc_no_public_cat.set_current_language('de')
        self.de_doc_no_public_cat.category = nonpub_cat
        self.de_doc_no_public_cat.is_published = False
        self.de_doc_no_public_cat.title = 'DE without published category'
        self.de_doc_no_public_cat.save()

    def test_manager(self):
        """Testing if the ``DocumentManager`` retrieves the correct objects."""
        request = Mock(LANGUAGE_CODE='en')
        self.assertEqual(
            models.Document.objects.published(request).count(), 1, msg=(
                'In English, there should be one published document.'))

        request = Mock(LANGUAGE_CODE='de')
        self.assertEqual(
            models.Document.objects.published(request).count(), 1, msg=(
                'In German, there should be one published document.'))

        request = Mock(LANGUAGE_CODE=None)
        self.assertEqual(
            models.Document.objects.published(request).count(), 0, msg=(
                'If no language is set, there should be no published'
                ' documents.'))


class DocumentPluginTestCase(TestCase):
    """Tests for the ``DocumentPlugin`` model."""
    longMessage = True

    def test_model(self):
        doc = baker.make('document_library.Document')
        instance = models.DocumentPlugin(document=doc)
        instance.save()
        self.assertTrue(instance.pk, msg=('Should be able to instantiate and save the object.'))
