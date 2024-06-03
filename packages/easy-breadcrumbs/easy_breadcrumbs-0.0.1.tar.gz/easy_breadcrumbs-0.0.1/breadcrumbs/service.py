import logging

from django.urls import resolve, reverse
from django.urls.exceptions import Resolver404

from .utils import get_breadcrumbs_settings

logger = logging.getLogger(__name__)


def get_breadcrumbs(request):
    settings = get_breadcrumbs_settings()
    title_field = settings['title_field']

    request._breadcrumbs_generating = True
    breadcrumbs = [{'title': 'Главная', 'url': reverse(settings['homepage_url'])}]
    current_path = request.path
    url_parts = [part for part in current_path.split('/') if part]
    url = '/'

    for i, url_part in enumerate(url_parts):
        url += url_part + '/'

        try:
            resolved = resolve(url)
            name, namespace = resolved.url_name, resolved.namespace
            response = resolved.func(request, **resolved.kwargs)
            title = response.context_data.get(title_field, '')

            if i == len(url_parts) - 1:
                # For the last crumb we do not create a link.
                breadcrumbs.append({'title': title, 'url': None})
            else:
                # We form a backlink taking into the namespace and
                # passed arguments (slugs).
                if namespace:
                    url_name = f'{namespace}:{name}'
                else:
                    url_name = name

                breadcrumbs.append({
                    'title': title,
                    'url': reverse(url_name, kwargs=resolved.kwargs),
                })

        except Resolver404:
            continue
        except Exception as e:
            logger.error(f'Error generating breadcrumb for {url}: {e}')
            continue

    del request._breadcrumbs_generating
    return breadcrumbs
