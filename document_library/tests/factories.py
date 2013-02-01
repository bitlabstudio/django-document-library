"""Factories for the ``document_library`` app."""
import factory

from document_library.models import Document, DocumentTitle


class DocumentFactory(factory.Factory):
    """Factory for the ``Document`` model."""
    FACTORY_FOR = Document

    is_published = True


class DocumentTitleFactoryBase(factory.Factory):
    """Base factory for factories for ``DocumentTitle`` models."""
    FACTORY_FOR = DocumentTitle

    document = factory.SubFactory(DocumentFactory)


class DocumentTitleENFactory(DocumentTitleFactoryBase):
    """Factory for english ``DocumentTitle`` objects."""
    title = 'A title'
    language = 'en'


class DocumentTitleDEFactory(DocumentTitleFactoryBase):
    """Factory for english ``DocumentTitle`` objects."""
    title = 'Ein Titel'
    language = 'de'
