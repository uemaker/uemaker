from django import template
from urllib import parse
import urllib
from django.http import QueryDict

register = template.Library()

@register.filter()
def url_match(url, module):
    if '/' + module in url:
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