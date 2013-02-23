"""CMS apphook for the ``document_library`` app."""
from django.utils.translation import ugettext_lazy as _

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool


class DocumentLibraryApphook(CMSApp):
    name = _("Document Library Apphook")
    urls = ["document_library.urls"]


apphook_pool.register(DocumentLibraryApphook)
