"""Admin classes for the ``document_library`` app."""
from django.contrib import admin
from django.utils.translation import get_language
from django.utils.translation import ugettext_lazy as _

from simple_translation.admin import TranslationAdmin
from simple_translation.utils import get_preferred_translation_from_lang

from document_library.models import Document, DocumentCategory


class DocumentCategoryAdmin(TranslationAdmin):
    """Admin class for the ``DocumentCategory`` model."""
    list_display = ['title', 'languages', ]

    def title(self, obj):
        lang = get_language()
        return get_preferred_translation_from_lang(obj, lang).title
    title.short_description = _('Title')


class DocumentAdmin(TranslationAdmin):
    """Admin class for the ``Document`` model."""
    list_display = ['title', 'position', 'user', 'languages', ]

    def title(self, obj):
        lang = get_language()
        return get_preferred_translation_from_lang(obj, lang).title
    title.short_description = _('Title')


admin.site.register(Document, DocumentAdmin)
admin.site.register(DocumentCategory, DocumentCategoryAdmin)
