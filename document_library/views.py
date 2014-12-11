"""Views for the ``document_library`` app."""
from datetime import date

from django.contrib.auth.decorators import login_required
from django.db import connection, models
from django.http import Http404
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView

from dateutil import relativedelta
from django_libs.utils import conditional_decorator

from .models import Document, DocumentCategory
from . import settings


class DocumentListMixin(object):
    """Mixin to provide document list functions."""
    paginate_by = settings.PAGINATION_AMOUNT

    @conditional_decorator(
        method_decorator(login_required), settings.LOGIN_REQUIRED)
    def dispatch(self, request, *args, **kwargs):
        return super(DocumentListMixin, self).dispatch(
            request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(DocumentListMixin, self).get_context_data(**kwargs)
        ctx.update({
            'categories': DocumentCategory.objects.all(),
            'months': self.months,
        })
        return ctx

    def get_queryset(self):
        truncate_date = connection.ops.date_trunc_sql('month', 'document_date')
        qs = Document.objects.published(self.request).extra({
            'month': truncate_date})
        self.months = qs.values('month').annotate(
            models.Count('pk')).order_by('-month')
        if settings.PAGINATE_BY_CATEGORIES:
            categories = DocumentCategory.objects.all()
            max_amount = 0
            item_range = settings.PAGINATION_AMOUNT / categories.count()
            end_amount = qs.count()
            pks = []
            while max_amount < end_amount:
                for category in categories:
                    package = qs.filter(category=category)[
                        max_amount:max_amount + item_range].values_list(
                            'pk', flat=True)
                    pks += package
                max_amount += item_range
            clauses = ' '.join(
                ['WHEN id=%s THEN %s' % (pk, i) for i, pk in enumerate(pks)])
            ordering = 'CASE %s END' % clauses
            qs = Document.objects.filter(pk__in=pks).extra(
                select={'ordering': ordering}, order_by=('ordering',))
        return qs


class DocumentListView(DocumentListMixin, ListView):
    """A view that lists all documents for the current language."""
    pass


class DocumentDetailView(DetailView):
    """A view that displays detailed information about an event."""
    model = Document

    @conditional_decorator(
        method_decorator(login_required), settings.LOGIN_REQUIRED)
    def dispatch(self, request, *args, **kwargs):
        return super(DocumentDetailView, self).dispatch(
            request, *args, **kwargs)


class DocumentMonthView(DocumentListMixin, ListView):
    """A view that lists a month's documents for the current language."""
    template_name = 'document_library/document_month.html'

    def dispatch(self, request, *args, **kwargs):
        try:
            self.month = date(
                int(kwargs.get('year')), int(kwargs.get('month')), 1)
        except ValueError:
            raise Http404
        return super(DocumentMonthView, self).dispatch(
            request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(DocumentMonthView, self).get_context_data(**kwargs)
        last_month = self.month - relativedelta.relativedelta(months=1)
        next_month = self.month + relativedelta.relativedelta(months=1)
        if next_month > date.today():
            next_month = None

        ctx.update({
            'month': self.month,
            'last_month': last_month,
            'next_month': next_month,
        })
        return ctx

    def get_queryset(self):
        qs = super(DocumentMonthView, self).get_queryset()
        return qs.filter(
            document_date__year=self.month.year,
            document_date__month=self.month.month,
        )
