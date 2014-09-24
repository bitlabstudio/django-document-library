"""Templatetags for the ``document_library`` app."""
from django import template

from document_library.models import Document


register = template.Library()


@register.assignment_tag
def get_files_for_document(document):
    """
    Returns the available files for all languages.

    In case the file is already present in another language, it does not re-add
    it again.

    """
    files = []
    for doc_trans in document.translations.all():
        if doc_trans.filer_file is not None and \
                doc_trans.filer_file not in files:
            doc_trans.filer_file.language = doc_trans.language_code
            files.append(doc_trans.filer_file)
    return files


@register.assignment_tag(takes_context=True)
def get_frontpage_documents(context):
    """Returns the library favs that should be shown on the front page."""
    req = context.get('request')
    qs = Document.objects.published(req).filter(is_on_front_page=True)
    return qs


@register.assignment_tag(takes_context=True)
def get_latest_documents(context, count=5):
    """
    Returns the latest documents.

    :param count: Number of documents to be returned. Defaults to 5.

    """
    req = context.get('request')
    qs = Document.objects.published(req)[:count]
    return qs
