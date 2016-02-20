"""Tests for the views of the ``document_library`` app."""
from django.utils import timezone
from django.test import TestCase, RequestFactory

from django_libs.tests.mixins import ViewRequestFactoryTestMixin
from mixer.backend.django import mixer

from .. import views


class DocumentListViewTestCase(ViewRequestFactoryTestMixin, TestCase):
    """Tests for the ``DocumentListView`` view."""
    def setUp(self):
        self.document = mixer.blend('document_library.DocumentTranslation')
        self.view_class = views.DocumentListView

    def test_view(self):
        self.is_callable()


class DocumentDetailViewTestCase(TestCase):
    """Tests for the ``DocumentDetailView`` view."""
    def test_view(self):
        doc = mixer.blend('document_library.DocumentTranslation')
        req = RequestFactory().get('/')
        resp = views.DocumentDetailView.as_view()(req, pk=doc.pk)
        self.assertEqual(resp.status_code, 200)


class DocumentMonthViewTestCase(ViewRequestFactoryTestMixin, TestCase):
    """Tests for the ``DocumentMonthView`` view."""
    def setUp(self):
        self.document = mixer.blend(
            'document_library.DocumentTranslation').master
        self.view_class = views.DocumentMonthView

    def get_view_kwargs(self):
        self.document.document_date = timezone.now()
        return {
            'month': self.document.document_date.month,
            'year': self.document.document_date.year,
        }

    def test_view(self):
        self.is_callable()
        self.is_not_callable(kwargs={'month': 13, 'year': 2014})
