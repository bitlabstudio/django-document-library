"""Templatetags for the ``document_library`` app."""
from django import template

from document_library.models import Document, DocumentTitle


register = template.Library()


@register.assignment_tag
def get_files_for_document(document):
    """Returns all available files for the given document."""
    titles = DocumentTitle.objects.filter(
        document=document, filer_file__isnull=False)
    files = [title.filer_file for title in titles]
    return files


@register.assignment_tag(takes_context=True)
def get_frontpage_documents(context):
    """Returns the library favs that should be shown on the front page."""
    req = context.get('request')
    qs = Document.objects.published(req).filter(is_on_front_page=True)
    return qs
