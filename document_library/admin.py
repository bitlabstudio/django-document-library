"""Admin classes for the ``document_library`` app."""
from django.contrib import admin
from django.contrib.contenttypes.generic import GenericTabularInline
from django.utils.translation import get_language
from django.utils.translation import ugettext_lazy as _

from cmsplugin_blog.admin import M2MPlaceholderAdmin
from django_libs.admin import MultilingualPublishMixin
from simple_translation.admin import TranslationAdmin
from simple_translation.utils import get_preferred_translation_from_lang

from .models import Attachment, Document, DocumentCategory


class AttachmentInline(GenericTabularInline):
    model = Attachment
    extra = 1
    raw_id_fields = ['document', ]


class DocumentCategoryAdmin(TranslationAdmin):
    """Admin class for the ``DocumentCategory`` model."""
    list_display = ['title', 'languages', ]

    def title(self, obj):
        lang = get_language()
        return get_preferred_translation_from_lang(obj, lang).title
    title.short_description = _('Title')


class DocumentAdmin(MultilingualPublishMixin, M2MPlaceholderAdmin):
    """Admin class for the ``Document`` model."""
    list_display = [
        'title', 'position', 'user', 'is_on_front_page', 'languages',
        'is_published']

    def title(self, obj):
        lang = get_language()
        return get_preferred_translation_from_lang(obj, lang).title
    title.short_description = _('Title')


admin.site.register(Document, DocumentAdmin)
admin.site.register(DocumentCategory, DocumentCategoryAdmin)
