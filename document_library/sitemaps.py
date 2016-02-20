"""Sitemaps for the `multilingual_news` app."""
from django.contrib.sitemaps import Sitemap

from .models import Document


class DocumentSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return Document.objects.published()

    def lastmod(self, obj):
        return obj.creation_date
