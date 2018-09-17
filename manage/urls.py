"""uemaker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^demo/$', views.DemoView.as_view(), name='demo'),
    url(r'^system/modules/$', views.ModuleListView.as_view(), name='modules'),
    url(r'^system/add_module/$', views.ModuleCreateView.as_view(), name='add_module'),
    url(r'^system/edit_module/(?P<pk>\d+)/$', views.ModuleUpdateView.as_view(), name='edit_module'),
    url(r'^system/fields/(?P<mid>\d+)/$', views.FieldListView.as_view(), name='fields'),
    url(r'^system/add_field/(?P<mid>\d+)/$', views.FieldCreateView.as_view(), name='add_field'),
    url(r'^system/edit_field/(?P<pk>\d+)/$', views.FieldUpdateView.as_view(), name='edit_field'),
    url(r'^module/(?P<module_name>\w+)/category/$', views.CategoryListView.as_view(), name='category'),
    url(r'^module/(?P<module_name>\w+)/category/add/$', views.CategoryCreateView.as_view(), name='add_category'),
    url(r'^module/(?P<module_name>\w+)/category/edit/(?P<pk>\d+)/$', views.CategoryUpdateView.as_view(), name='edit_category'),
    url(r'^module/(?P<module_name>\w+)/list/$', views.MatrixListView.as_view(), name='matrix'),
    url(r'^module/(?P<module_name>\w+)/add/$', views.MatrixCreateView.as_view(), name='add_matrix'),
    url(r'^module/(?P<module_name>\w+)/edit/(?P<pk>\d+)/$', views.MatrixUpdateView.as_view(), name='edit_matrix'),
]
