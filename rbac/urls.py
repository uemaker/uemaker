from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^users/$', views.UserListView.as_view(), name='users'),
    url(r'^user/add_user/$', views.UserCreateView.as_view(), name='add_user'),
    url(r'^user/edit_user/(?P<pk>\w+)/$', views.UserUpdateView.as_view(), name='edit_user'),
]