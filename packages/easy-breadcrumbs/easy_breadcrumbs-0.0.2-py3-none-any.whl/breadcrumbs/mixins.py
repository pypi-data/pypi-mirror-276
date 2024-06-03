from django.views.generic.base import ContextMixin

from .service import get_breadcrumbs


class BreadcrumbsMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request

        if hasattr(request, '_breadcrumbs_generating'):
            return context

        crumbs = get_breadcrumbs(request)
        context['breadcrumbs'] = crumbs
        return context
