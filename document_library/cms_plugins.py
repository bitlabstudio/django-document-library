"""django-cms plugin for the ``document_library`` app."""
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _

from . import models


class DocumentLibraryPlugin(CMSPluginBase):
    model = models.DocumentPlugin
    name = _('Document Library Plugin')
    render_template = "document_library/document_library_plugin.html"

    def render(self, context, instance, placeholder):
        context.update({
            'document': instance.document,
            'categories': models.DocumentCategory.objects.all(),
        })
        return context


plugin_pool.register_plugin(DocumentLibraryPlugin)
