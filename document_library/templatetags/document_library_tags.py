"""Templatetags for the ``document_library`` app."""
from django import template

from document_library.models import DocumentTitle


register = template.Library()


@register.assignment_tag
def get_files_for_document(document):
    """Returns all available files for the given document."""
    titles = DocumentTitle.objects.filter(
        document=document, filer_file__isnull=False)
    files = [title.filer_file for title in titles]
    return files
