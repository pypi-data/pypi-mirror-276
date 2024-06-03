from django import template

register = template.Library()


@register.inclusion_tag('breadcrumbs/templates/breadcrumbs/breadcrumbs.html', takes_context=True)
def show_breadcrumbs(context):
    return {'breadcrumbs': context.get('breadcrumbs', [])}
