# -*- coding: utf-8 -*-
"""Tests for the models of the ``document_library`` app."""
from __future__ import unicode_literals

from mock import Mock

from django.test import TestCase

from mixer.backend.django import mixer

from .. import models


class AttachmentTestCase(TestCase):
    """Tests for the ``Attachment`` model."""
    longMessage = True

    def test_model(self):
        obj = mixer.blend('document_library.Attachment')
        self.assertTrue(obj.pk, msg=(
            'Should be able to instantiate and save the model.'))


class DocumentTestCase(TestCase):
    """Tests for the ``Document`` model."""
    longMessage = True

    def test_model(self):
        instance = mixer.blend('document_library.DocumentTranslation')
        self.assertTrue(instance.pk, msg=(
            'Should be able to instantiate and save the object.'))

    def test_get_filetype(self):
        instance = mixer.blend('document_library.DocumentTranslation',
                               language_code='en').master
        self.assertEqual(instance.get_filetype(), '', msg=(
            'Should return the filetype.'))

        instance.filer_file = mixer.blend('filer.File')
        self.assertEqual(instance.get_filetype(), '', msg=(
            'Should return the filetype.'))


class DocumentCategoryTestCase(TestCase):
    """Tests for the ``DocumentCategory`` model."""
    longMessage = True

    def test_model(self):
        instance = mixer.blend(
            'document_library.DocumentCategoryTranslation').master
        self.assertTrue(instance.pk, msg=(
            'Should be able to instantiate and save the object.'))

    def test_get_title(self):
        instance = mixer.blend('document_library.DocumentCategoryTranslation')
        result = instance.master.get_title()
        self.assertTrue(result, msg=('Should return the translated title.'))


class DocumentManagerTestCase(TestCase):
    """Tests for the ``DocumentManager`` model manager."""
    longMessage = True

    def setUp(self):
        self.en_doc = mixer.blend(
            'document_library.DocumentTranslation',
            category=mixer.blend(
                'document_library.DocumentCategoryTranslation',
                is_published=True),
            language_code='en', is_published=False)
        self.de_doc = mixer.blend(
            'document_library.DocumentTranslation',
            category=mixer.blend(
                'document_library.DocumentCategoryTranslation',
                is_published=True),
            language_code='de', is_published=False)
        self.de_doc_no_public_cat = mixer.blend(
            'document_library.DocumentTranslation',
            category=mixer.blend(
                'document_library.DocumentCategoryTranslation',
                is_published=False),
            language_code='de', is_published=False)
        new_doc = self.de_doc.master.translate('en')
        new_doc.is_published = True
        new_doc.save()
        new_doc = self.en_doc.master.translate('de')
        new_doc.is_published = True
        new_doc.save()
        new_doc = self.de_doc_no_public_cat.master.translate('en')
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
        instance = models.DocumentPlugin(document=mixer.blend(
            'document_library.DocumentTranslation').master)
        instance.save()
        self.assertTrue(instance.pk, msg=(
            'Should be able to instantiate and save the object.'))
