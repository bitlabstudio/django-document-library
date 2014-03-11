"""Factories for the ``document_library`` app."""
import factory

from document_library.models import (
    Attachment,
    Document,
    DocumentCategory,
)
from document_library.tests.test_app.models import DummyModel


class DummyModelFactory(factory.Factory):
    """Factory for the ``DummyModel`` model."""
    FACTORY_FOR = DummyModel


class DocumentCategoryFactory(factory.Factory):
    """Factory for the ``DocumentCategory`` model."""
    FACTORY_FOR = DocumentCategory

    slug = factory.Sequence(lambda n: 'slug-{0}'.format(n))
    is_published = True
    title = factory.Sequence(lambda n: 'title {0}'.format(n))


class DocumentFactory(factory.Factory):
    """Factory for the ``Document`` model."""
    FACTORY_FOR = Document

    is_published = True
    title = factory.Sequence(lambda n: 'title {0}'.format(n))


class AttachmentFactory(factory.Factory):
    """Factory for the ``EntryAttachment`` model."""
    FACTORY_FOR = Attachment

    content_object = factory.SubFactory(DummyModelFactory)
    document = factory.SubFactory(DocumentFactory)
