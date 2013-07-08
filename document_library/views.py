"""Views for the ``document_library`` app."""
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView

from django_libs.utils import conditional_decorator

from .models import Document, DocumentCategory
from . import settings


class DocumentListView(ListView):
    """A view that lists all documents for the current language."""
    model = Document

    @conditional_decorator(
        method_decorator(login_required), settings.LOGIN_REQUIRED)
    def dispatch(self, request, *args, **kwargs):
        return super(DocumentListView, self).dispatch(request, *args, **kwargs)

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

    @conditional_decorator(
        method_decorator(login_required), settings.LOGIN_REQUIRED)
    def dispatch(self, request, *args, **kwargs):
        return super(DocumentDetailView, self).dispatch(
            request, *args, **kwargs)
