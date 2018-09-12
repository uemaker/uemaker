from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.urls import reverse
from django.db.models import Q
import json

from manage.models import Module
from manage.models import Category
from manage.forms import ModuleAddForm
from manage.forms import CategoryAddForm

class IndexView(TemplateView):

    template_name = 'manage/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        return context

class ModuleListView(ListView):
    # model = Module
    template_name = 'manage/system/module_list.html'
    context_object_name = "modules"
    paginate_by = 100

    def post(self, request):
        id_list = request.POST.getlist('id_list[]')
        data = {}
        if id_list:
            idstring = ','.join(id_list)
            Module.objects.extra(where=['id IN ('+ idstring +')']).delete()
            data['success'] = 1
        else:
            data['success'] = 0

        return HttpResponse(json.dumps(data), content_type="application/json")

    def get_queryset(self):
        listdata = Module.objects.all()
        keyword = self.request.GET.get('q')
        if keyword:
            listdata = listdata.filter(Q(name__icontains=keyword)|Q(title__icontains=keyword))
        return listdata

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ModuleListView, self).get_context_data(**kwargs)
        context['form_url'] = reverse('modules')
        context['q'] = self.request.GET.get('q', '')
        return context

class ModuleCreateView(CreateView):
    template_name = 'manage/system/create_form.html'
    form_class = ModuleAddForm
    success_url = 'modules'

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse(self.success_url))

    def get_context_data(self, **kwargs):
        context = super(ModuleCreateView, self).get_context_data(**kwargs)
        context['form_url'] = reverse('add_module')
        context['form_title'] = '创建模块'
        return context

class ModuleUpdateView(UpdateView):
    model = Module
    template_name = 'manage/system/create_form.html'
    form_class = ModuleAddForm
    success_url = 'modules'

    def get_context_data(self, **kwargs):
        context = super(ModuleUpdateView, self).get_context_data(**kwargs)
        context['form_url'] = reverse('edit_module', kwargs={'pk': self.kwargs.get(self.pk_url_kwarg)})
        context['form_title'] = '编辑模块'
        return context

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse(self.success_url))

class CategoryListView(ListView):
    # model = Module
    template_name = 'manage/system/category_list.html'
    context_object_name = "data"
    paginate_by = 2

    def post(self, request):
        id_list = request.POST.getlist('id_list[]')
        data = {}
        if id_list:
            idstring = ','.join(id_list)
            Category.objects.extra(where=['id IN ('+ idstring +')']).delete()
            data['success'] = 1
        else:
            data['success'] = 0

        return HttpResponse(json.dumps(data), content_type="application/json")

    def get_queryset(self):
        listdata = Category.objects.all()
        keyword = self.request.GET.get('q')
        if keyword:
            listdata = listdata.filter(Q(name__icontains=keyword)|Q(title__icontains=keyword))
        return listdata

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        context['form_url'] = reverse('categories')
        context['q'] = self.request.GET.get('q', '')
        return context

class CategoryCreateView(CreateView):
    form_class = CategoryAddForm
    template_name = 'manage/system/create_form.html'
    success_url = 'categories'

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse(self.success_url))

    def get_context_data(self, **kwargs):
        context = super(CategoryCreateView, self).get_context_data(**kwargs)
        context['form_url'] = reverse('add_category')
        context['form_title'] = '创建分类'
        return context

class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryAddForm
    template_name = 'manage/system/create_form.html'
    success_url = 'categories'

    def get_context_data(self, **kwargs):
        context = super(CategoryUpdateView, self).get_context_data(**kwargs)
        context['form_url'] = reverse('edit_category', kwargs={'pk': self.kwargs.get(self.pk_url_kwarg)})
        context['form_title'] = '编辑分类'
        return context

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse(self.success_url))
