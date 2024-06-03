from django.conf import settings


def get_breadcrumbs_settings():
    return {
        'homepage_url': getattr(settings, 'BREADCRUMBS_HOMEPAGE_URL', 'homepage:homepage'),
        'title_field': getattr(settings, 'BREADCRUMBS_TITLE_FIELD', 'title'),
    }
