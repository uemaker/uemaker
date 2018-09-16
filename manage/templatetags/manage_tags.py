from django import template
from urllib import parse
import urllib
from django.http import QueryDict
from manage.utils import FieldUtil

register = template.Library()

@register.filter()
def url_match(url, module):
    if module in url:
        return True
    else:
        return False

@register.simple_tag()
def url_set_param(url, name, value):
    q = {}
    if not url is None:
        result = parse.urlparse(url)
        p = QueryDict(result.query)
        q = p.dict()

    q[name] = str(value)
    return '?'+parse.urlencode(q)

@register.filter()
def field_type_text(filed_type):
    types = FieldUtil.FieldType
    if types and types.get(filed_type, None):
        return types.get(filed_type)
    else:
        return filed_type
