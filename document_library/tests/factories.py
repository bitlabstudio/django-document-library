"""Factories for the ``document_library`` app."""
import factory

from document_library.models import (
    Document,
    DocumentCategory,
    DocumentCategoryTitle,
    DocumentTitle,
)


class DocumentCategoryFactory(factory.Factory):
    """Factory for the ``DocumentCategory`` model."""
    FACTORY_FOR = DocumentCategory


class DocumentCategoryTitleFactoryBase(factory.Factory):
    """Base factory for factories for ``DocumentCategoryTitle`` models."""
    FACTORY_FOR = DocumentCategoryTitle

    category = factory.SubFactory(DocumentCategoryFactory)


class DocumentCategoryTitleENFactory(DocumentCategoryTitleFactoryBase):
    """Factory for english ``DocumentCategoryTitle`` objects."""
    title = 'A title'
    language = 'en'


class DocumentCategoryTitleDEFactory(DocumentCategoryTitleFactoryBase):
    """Factory for german ``DocumentCategoryTitle`` objects."""
    title = 'Ein Titel'
    language = 'de'


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
    """Factory for german ``DocumentTitle`` objects."""
    title = 'Ein Titel'
    language = 'de'
