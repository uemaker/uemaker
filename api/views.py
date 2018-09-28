import json

from django.core import serializers
from django.http.response import JsonResponse
from django.views.decorators.http import require_http_methods

from manage.models import Article
from manage.utils import JsonEncoder


@require_http_methods(["GET"])
def articleList(request):

    article_list = Article.objects.filter().values()
    json_list = []
    if article_list:
        for article in article_list:
            json_list.append(article.toDict())

    response = {}
    response['code'] = 0
    response['msg'] = ''
    response['data'] = json.dumps(json_list, cls=JsonEncoder)

    return JsonResponse(response, safe=False)