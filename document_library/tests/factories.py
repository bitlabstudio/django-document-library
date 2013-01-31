"""Factories for the ``document_library`` app."""
import factory

from document_library.models import Document, DocumentTitle


class DocumentFactory(factory.Factory):
    """Factory for the ``Document`` model."""
    FACTORY_FOR = Document


class DocumentTitleFactoryBase(factory.Factory):
    """Base factory for factories for ``DocumentTitle`` models."""
    FACTORY_FOR = DocumentTitle

    document = factory.SubFactory(DocumentFactory)


class DocumentTitleENFactory(DocumentTitleFactoryBase):
    """Factory for english ``DocumentTitle`` objects."""
    title = 'A title'
