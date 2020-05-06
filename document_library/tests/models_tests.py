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
        instance = baker.make('document_library.DocumentTranslation')
        self.assertTrue(instance.pk, msg=(
            'Should be able to instantiate and save the object.'))

    def test_get_filetype(self):
        self.de_doc = baker.make('document_library.DocumentTranslation')
        instance = self.de_doc.master.translate('de')

        self.assertEqual(
            instance.get_filetype(), '', msg='Should return the filetype.')

        instance.filer_file = baker.make('filer.File')
        instance.filer_file.file.name = 'image.jpg'
        self.assertEqual(instance.get_filetype(), 'JPG', msg=(
            'Should return the filetype.'))


class DocumentCategoryTestCase(TestCase):
    """Tests for the ``DocumentCategory`` model."""
    longMessage = True

    def test_model(self):
        instance = baker.make(
            'document_library.DocumentCategoryTranslation').master
        self.assertTrue(instance.pk, msg=(
            'Should be able to instantiate and save the object.'))

    def test_get_title(self):
        instance = baker.make('document_library.DocumentCategoryTranslation')
        result = instance.master.get_title()
        self.assertTrue(result, msg=('Should return the translated title.'))


class DocumentManagerTestCase(TestCase):
    """Tests for the ``DocumentManager`` model manager."""
    longMessage = True

    def setUp(self):
        de_cat = baker.make('document_library.DocumentCategory',
                            is_published=True)
        self.de_doc = baker.make('document_library.DocumentTranslation')
        new_doc = self.de_doc.master.translate('de')
        new_doc.category = de_cat
        new_doc.is_published = True
        new_doc.save()

        en_cat = baker.make('document_library.DocumentCategory',
                            is_published=True)
        self.en_doc = baker.make('document_library.DocumentTranslation')
        new_doc = self.en_doc.master.translate('en')
        new_doc.category = en_cat
        new_doc.is_published = True
        new_doc.save()

        nonpub_cat = baker.make(
            'document_library.DocumentCategory',
            is_published=False
        )
        self.de_doc_no_public_cat = baker.make(
            'document_library.DocumentTranslation')
        new_doc = self.de_doc_no_public_cat.master.translate('de')
        new_doc.category = nonpub_cat
        new_doc.is_published = False
        new_doc.save()

    def test_manager(self):
        """Testing if the ``DocumentManager`` retrieves the correct objects."""
        request = Mock(LANGUAGE_CODE='de')
        self.assertEqual(
            models.Document.objects.published(request).count(), 1, msg=(
                'In German, there should be one published document.'))

        request = Mock(LANGUAGE_CODE='en')
        self.assertEqual(
            models.Document.objects.published(request).count(), 1, msg=(
                'In English, there should be one published document.'))

        request = Mock(LANGUAGE_CODE=None)
        self.assertEqual(
            models.Document.objects.published(request).count(), 0, msg=(
                'If no language is set, there should be no published'
                ' documents.'))


class DocumentPluginTestCase(TestCase):
    """Tests for the ``DocumentPlugin`` model."""
    longMessage = True

    def test_model(self):
        instance = models.DocumentPlugin(document=baker.make(
            'document_library.DocumentTranslation').master)
        instance.save()
        self.assertTrue(instance.pk, msg=(
            'Should be able to instantiate and save the object.'))
