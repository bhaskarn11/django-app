from django import template
from django.utils.http import urlencode
register = template.Library()

@register.simple_tag(takes_context=True)
def current_query(context):
    d = context['request'].GET.dict()
    if d.get('page'):
        d.pop('page')
    return urlencode(d)
