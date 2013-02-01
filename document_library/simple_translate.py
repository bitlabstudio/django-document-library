"""Registration of models for simple-translation."""
from simple_translation.translation_pool import translation_pool

from document_library.models import (
    Document,
    DocumentCategory,
    DocumentCategoryTitle,
    DocumentTitle,
)


translation_pool.register_translation(Document, DocumentTitle)
translation_pool.register_translation(DocumentCategory, DocumentCategoryTitle)
