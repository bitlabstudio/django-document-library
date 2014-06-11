"""Factories for the ``document_library`` app."""
import factory

from django.utils.timezone import now

from dateutil.relativedelta import relativedelta
from filer.models.filemodels import File

from document_library.models import (
    Attachment,
    Document,
    DocumentCategory,
)
from document_library.tests.test_app.models import DummyModel


class DummyModelFactory(factory.DjangoModelFactory):
    """Factory for the ``DummyModel`` model."""
    FACTORY_FOR = DummyModel


class DocumentCategoryFactory(factory.DjangoModelFactory):
    """Factory for the ``DocumentCategory`` model."""
    FACTORY_FOR = DocumentCategory

    slug = factory.Sequence(lambda n: 'slug-{0}'.format(n))
    is_published = True
    title = factory.Sequence(lambda n: 'title {0}'.format(n))


class DocumentFactory(factory.DjangoModelFactory):
    """Factory for the ``Document`` model."""
    FACTORY_FOR = Document

    is_published = True
    title = factory.Sequence(lambda n: 'title {0}'.format(n))
    document_date = factory.Sequence(lambda n: now() - relativedelta(days=1))
    category = factory.SubFactory(DocumentCategoryFactory)


class AttachmentFactory(factory.DjangoModelFactory):
    """Factory for the ``EntryAttachment`` model."""
    FACTORY_FOR = Attachment

    content_object = factory.SubFactory(DummyModelFactory)
    document = factory.SubFactory(DocumentFactory)


class FileFactory(factory.DjangoModelFactory):
    """Factory for the ``File`` model."""
    FACTORY_FOR = File

    file = factory.Sequence(lambda n: 'file_{0}'.format(n))
