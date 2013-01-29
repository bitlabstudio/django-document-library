"""Admin classes for the ``document_library`` app."""
from django.contrib import admin
from django.utils.translation import get_language
from django.utils.translation import ugettext_lazy as _

from simple_translation.admin import TranslationAdmin
from simple_translation.utils import get_translation_queryset

from document_library.models import Document


class DocumentAdmin(TranslationAdmin):
    """Admin class for the ``Document`` model."""
    list_display = ['title', 'position', 'user', 'languages', ]

    def title(self, obj):
        lang = get_language()
        return get_translation_queryset(obj).filter(language=lang)[0].title
    title.short_description = _('Title')


admin.site.register(Document, DocumentAdmin)
