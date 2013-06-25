"""Models for the ``document_library`` app."""
from django.conf import settings
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import get_language
from django.utils.translation import ugettext_lazy as _

from cms.models.pluginmodel import CMSPlugin
from django_libs.models_mixins import SimpleTranslationMixin
from djangocms_utils.fields import M2MPlaceholderField
from filer.fields.file import FilerFileField
from simple_translation.actions import SimpleTranslationPlaceholderActions
from simple_translation.utils import get_preferred_translation_from_lang


class Attachment(models.Model):
    """
    Mapping class to map any object to ``Document`` objects.

    This allows you to add inlines to your admins and attach documents to
    your objects.

    """
    document = models.ForeignKey(
        'document_library.Document',
        verbose_name=_('Document'),
    )

    position = models.PositiveIntegerField(
        verbose_name=_('Position'),
        null=True, blank=True,
    )

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ['position', ]


class DocumentCategory(SimpleTranslationMixin, models.Model):
    """
    Documents can be grouped in categories.

    See ``DocumentCategoryTitle`` for translateable fields.

    :creation_date: The DateTime when this category was created.

    """
    creation_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Creation date'),
    )

    slug = models.SlugField(
        max_length=32,
        verbose_name=_('Slug'),
    )

    def __unicode__(self):
        return self.get_title()

    def get_title(self):
        lang = get_language()
        return get_preferred_translation_from_lang(self, lang).title


class DocumentCategoryTitle(models.Model):
    """
    Translateable fields for the ``DocumentCategory`` model.

    :title: The title of this category.

    """
    title = models.CharField(
        max_length=256,
        verbose_name=_('Title'),
    )

    # Needed by simple-translation
    category = models.ForeignKey(
        DocumentCategory, verbose_name=_('Category'))

    language = models.CharField(
        max_length=2, verbose_name=_('Language'), choices=settings.LANGUAGES)


class DocumentManager(models.Manager):
    """Custom manager for the ``Document`` model."""
    def published(self, request):
        """
        Returns the published documents in the current language.

        :param request: A Request instance.

        """
        language = getattr(request, 'LANGUAGE_CODE', None)
        if not language:
            return self.model.objects.none()

        qs = self.get_query_set()
        qs = qs.filter(
            documenttitle__is_published=True,
            documenttitle__language=language,
        )
        return qs


class DocumentPlugin(CMSPlugin):
    """Class to extend the `CMSPlugin` pluginmodel."""
    document = models.ForeignKey(
        'document_library.Document',
        verbose_name=_('Document'),
    )


class Document(SimpleTranslationMixin, models.Model):
    """
    A document consists of a title and description and a number of filer-files.

    See ``DocumentTitle`` for the translateable fields of this model.

    :creation_date: DateTime when this document was created.
    :user: Optional FK to the User who created this document.
    :position: If you want to order the documents other than by creation date,
      enter numbers for positioning here.
      views.
    :is_on_front_page: If ``True`` the object will be returned by the
      ``get_frontpage_documents`` templatetag.

    """
    category = models.ForeignKey(
        DocumentCategory,
        verbose_name=_('Category'),
        null=True, blank=True,
    )

    creation_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Creation date'),
    )

    user = models.ForeignKey(
        'auth.User',
        verbose_name=_('User'),
        null=True, blank=True,
    )

    position = models.PositiveIntegerField(
        verbose_name=_('Position'),
        null=True, blank=True,
    )

    is_on_front_page = models.BooleanField(
        default=False,
        verbose_name=('Is on front page'),
    )

    source_url = models.URLField(
        verbose_name=_('Source URL'),
        help_text=_(
            'Use this if you want to give credit for a downloadable file.'),
        blank=True,
    )

    download_url = models.URLField(
        verbose_name=_('Download URL'),
        help_text=_(
            'Use this if you want to link to a file instead of self-hosting'
            ' it'),
        blank=True,
    )

    placeholders = M2MPlaceholderField(
        actions=SimpleTranslationPlaceholderActions(),
        placeholders=('content', ),
    )

    creation_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Creation date'),
    )

    update_date = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Update date'),
    )

    objects = DocumentManager()

    class Meta:
        ordering = ('position', '-creation_date', )

    def __unicode__(self):
        return self.get_title()

    def get_absolute_url(self):
        return reverse('document_library_detail', kwargs={
            'pk': self.pk, })

    def get_filetype(self):
        lang = get_language()
        title = get_preferred_translation_from_lang(self, lang)
        if title.filer_file:
            return title.filer_file.extension.upper()
        return None

    def get_title(self):
        lang = get_language()
        return get_preferred_translation_from_lang(self, lang).title


class DocumentTitle(models.Model):
    """
    The translateable fields of the ``Document`` model.

    :title: The title of the document.
    :description: A short description of the document.
    :filer_file: FK to the File of the document version for this language.
    :is_published: If ``False`` the object will be excluded from the library
    :meta_description: The meta description to display for the detail page.

    """
    title = models.CharField(
        max_length=512,
        verbose_name=_('Title'),
    )

    description = models.TextField(
        verbose_name=_('Short description'),
        blank=True,
    )

    filer_file = FilerFileField(
        verbose_name=_('File'),
        null=True, blank=True,
    )

    copyright_notice = models.CharField(
        max_length=1024,
        verbose_name=_('Copyright notice'),
        blank=True,
    )

    is_published = models.BooleanField(
        verbose_name=_('Is published'),
        default=False,
    )

    meta_description = models.TextField(
        max_length=512,
        verbose_name=_('Meta description'),
        blank=True,
    )

    # Needed by simple-translation
    document = models.ForeignKey(
        Document, verbose_name=_('Document'))

    language = models.CharField(
        max_length=5, verbose_name=('Language'), choices=settings.LANGUAGES)

    def get_meta_description(self):
        if self.meta_description:
            return self.meta_description
        if len(self.description) > 160:
            return '{}...'.format(self.description[:160])
        return self.description
