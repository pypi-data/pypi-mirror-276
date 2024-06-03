import logging

from .service import get_breadcrumbs

logger = logging.getLogger(__name__)


def breadcrumbs(request):
    if hasattr(request, '_breadcrumbs_generating'):
        return {}

    crumbs = get_breadcrumbs(request)
    return {'breadcrumbs': crumbs}
