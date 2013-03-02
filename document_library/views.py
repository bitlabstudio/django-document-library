"""Views for the ``document_library`` app."""
from django.views.generic import DetailView, ListView

from .models import Document, DocumentCategory


class DocumentListView(ListView):
    """A view that lists all documents for the current language."""
    model = Document

    def get_context_data(self, **kwargs):
        ctx = super(DocumentListView, self).get_context_data(**kwargs)
        ctx.update({
            'categories': DocumentCategory.objects.all(),
        })
        return ctx

    def get_queryset(self):
        return Document.objects.published(self.request)


class DocumentDetailView(DetailView):
    """A view that displays detailed information about an event."""
    model = Document
