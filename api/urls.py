from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^article/list/$', views.articleList),
    url(r'^article/detail/(?P<id>\d+)/$', views.articleDetail),
]
