from django.forms import model_to_dict
from django.http.response import JsonResponse
from django.views.decorators.http import require_http_methods

from manage.models import Article, ArticleContent


@require_http_methods(["GET"])
def articleList(request):

    article_list = Article.objects.values()

    response = {}
    response['code'] = 0
    response['msg'] = ''
    response['data'] = list(article_list)

    return JsonResponse(response, safe=False)


@require_http_methods(["GET"])
def articleDetail(request, id):

    detail = {}
    if id:
        detail = Article.objects.filter(id=id).values('id', 'cat_id', 'title', 'desc', 'author', 'source', 'status', 'pub_time', 'create_time')
        content = ArticleContent.objects.get(id=id)
        print(content.content)
        if detail:
            detail = list(detail)[0]
            detail['content'] = content.content

    response = {}
    response['code'] = 0
    response['msg'] = ''
    response['data'] = detail
    print(response)

    return JsonResponse(response, safe=False)
