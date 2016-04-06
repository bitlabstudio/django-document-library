"""Models for the ``document_library`` app."""
from __future__ import unicode_literals

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import get_language, ugettext_lazy as _

from cms.models.fields import PlaceholderField
from cms.models.pluginmodel import CMSPlugin
from hvad.models import TranslatedFields, TranslatableModel, TranslationManager
from filer.fields.file import FilerFileField
from filer.fields.image import FilerImageField
from filer.fields.folder import FilerFolderField


@python_2_unicode_compatible
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
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ['position', ]

    def __str__(self):
        return self.document.get_title()


@python_2_unicode_compatible
class DocumentCategory(TranslatableModel):
    """
    Documents can be grouped in categories.

    :creation_date: The DateTime when this category was created.
    :slug: The slug of this category. E.g. used for filtering.
    :is_published: If the category should be visible to the public.

    translated:
    :title: The title of this category.

    """
    creation_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Creation date'),
    )

    slug = models.SlugField(
        max_length=32,
        verbose_name=_('Slug'),
    )

    is_published = models.BooleanField(
        verbose_name=_('Is published'),
        default=False,
    )

    translations = TranslatedFields(
        title=models.CharField(
            max_length=256,
            verbose_name=_('Title'),
        )
    )

    def __str__(self):
        return self.get_title()

    def get_title(self):
        return self.safe_translation_getter('title', self.slug)


class DocumentManager(TranslationManager):
    """Custom manager for the ``Document`` model."""
    def published(self, request=None):
        """
        Returns the published documents in the current language.

        :param request: A Request instance.

        """
        language = getattr(request, 'LANGUAGE_CODE', get_language())
        if not language:
            return self.model.objects.none()

        qs = self.get_queryset()
        qs = qs.filter(
            translations__is_published=True,
            translations__language_code=language,
        )
        # either it has no category or the one it has is published
        qs = qs.filter(
            models.Q(category__isnull=True) |
            models.Q(category__is_published=True))
        return qs


class DocumentPlugin(CMSPlugin):
    """Class to extend the `CMSPlugin` pluginmodel."""
    document = models.ForeignKey(
        'document_library.Document',
        verbose_name=_('Document'),
    )


@python_2_unicode_compatible
class Document(TranslatableModel):
    """
    A document consists of a title and description and a number of filer-files.

    :creation_date: DateTime when this Document object was created.
    :user: Optional FK to the User who created this document.
    :position: If you want to order the documents other than by creation date,
      enter numbers for positioning here.
      views.
    :is_on_front_page: If ``True`` the object will be returned by the
      ``get_frontpage_documents`` templatetag.
    :document_date: The date of the document itself. Don't confuse this with
      creation_date.
    :image: Document image. E.g. scan, cover.
    :folder: Filer folder to e.g. display a gallery.

    translated:
    :title: The title of the document.
    :description: A short description of the document.
    :filer_file: FK to the File of the document version for this language.
    :thumbnail: A thumbnail for the document.
    :is_published: If ``False`` this language will be excluded from the library
    :meta_description: The meta description to display for the detail page.

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
        settings.AUTH_USER_MODEL,
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

    content = PlaceholderField(
        'document_library_content',
        related_name='documents',
    )

    update_date = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Update date'),
    )

    document_date = models.DateTimeField(
        verbose_name=_('Document date'),
        blank=True, null=True,
    )

    image = FilerImageField(
        verbose_name=_('Image'),
        related_name='document_images',
        null=True, blank=True,
    )

    folder = FilerFolderField(
        verbose_name=_('Folder'),
        related_name='document_folders',
        null=True, blank=True,
    )

    translations = TranslatedFields(
        title=models.CharField(
            max_length=512,
            verbose_name=_('Title'),
        ),
        description=models.TextField(
            verbose_name=_('Short description'),
            blank=True,
        ),
        filer_file=FilerFileField(
            verbose_name=_('File'),
            related_name='document_files',
            null=True, blank=True,
        ),
        thumbnail=FilerFileField(
            verbose_name=_('Thumbnail'),
            related_name='document_thumbnails',
            null=True, blank=True,
        ),
        copyright_notice=models.CharField(
            max_length=1024,
            verbose_name=_('Copyright notice'),
            blank=True,
        ),
        is_published=models.BooleanField(
            verbose_name=_('Is published'),
            default=False,
        ),
        meta_description=models.TextField(
            max_length=512,
            verbose_name=_('Meta description'),
            blank=True,
        ),
    )

    objects = DocumentManager()

    class Meta:
        ordering = ('position', '-document_date', )

    def __str__(self):
        return self.get_title()

    def get_absolute_url(self):
        return reverse('document_library_detail', kwargs={
            'pk': self.pk, })

    def get_filetype(self):
        try:
            return self.filer_file.extension.upper()
        except AttributeError:
            return ''

    def get_title(self):
        # Kept for backwards compatibility
        return self.title
