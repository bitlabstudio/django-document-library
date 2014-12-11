"""Default settings for the document_library app."""
from django.conf import settings


LOGIN_REQUIRED = getattr(settings, 'DOCUMENT_LIBRARY_LOGIN_REQUIRED', False)
PAGINATION_AMOUNT = getattr(settings, 'DOCUMENT_LIBRARY_PAGINATION_AMOUNT', 1)
PAGINATE_BY_CATEGORIES = getattr(
    settings, 'DOCUMENT_LIBRARY_PAGINATE_BY_CATEGORIES', False)
