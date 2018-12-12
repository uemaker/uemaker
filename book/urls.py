from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^books/$', views.BookListView.as_view(), name='books'),
    url(r'^add_book/$', views.BookCreateView.as_view(), name='add_book'),
    url(r'^edit_book/(?P<pk>\w+)/$', views.BookUpdateView.as_view(), name='edit_book'),
    url(r'^chapters/(?P<bid>\d+)/$', views.ChapterListView.as_view(), name='chapters'),
    url(r'^add_chapter/(?P<bid>\d+)/$', views.ChapterCreateView.as_view(), name='add_chapter'),
    url(r'^edit_chapter/(?P<pk>\w+)/$', views.ChapterUpdateView.as_view(), name='edit_chapter'),
]