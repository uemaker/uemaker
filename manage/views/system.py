import json

from django.db.models import Q
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.base import TemplateView
from django.views.generic.base import View
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView

from manage.forms import ModuleFieldForm
from manage.forms import ModuleForm
from manage.models import FieldItem
from manage.models import Module
from manage.models import ModuleField
from manage.utils import FieldUtil
from manage.utils import ModuleUtil
from rbac import models


class DemoView(View):

    def get(self, request, *args, **kwargs):
        models.User.objects.create_user('atao', '', '123456')

        return HttpResponse('{}')


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

    def post(self, request, **kwargs):
        id_list = request.POST.getlist('id_list[]')
        data = {}
        if id_list:
            idstring = ','.join(id_list)
            Module.objects.extra(where=['id IN (' + idstring + ')', 'is_system = 0']).delete()
            data['success'] = 1
        else:
            data['success'] = 0

        return HttpResponse(json.dumps(data), content_type="application/json")

    def get_queryset(self):
        listdata = Module.objects.all()
        keyword = self.request.GET.get('q')
        if keyword:
            listdata = listdata.filter(Q(name__icontains=keyword) | Q(title__icontains=keyword))
        return listdata

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ModuleListView, self).get_context_data(**kwargs)
        context['form_url'] = reverse('modules')
        context['q'] = self.request.GET.get('q', '')
        return context


class ModuleCreateView(CreateView):
    template_name = 'manage/form/create_form.html'
    form_class = ModuleForm
    success_url = 'modules'

    def form_valid(self, form):
        if form.is_valid:
            form.save()
            return HttpResponseRedirect(reverse(self.success_url))

    def get_context_data(self, **kwargs):
        context = super(ModuleCreateView, self).get_context_data(**kwargs)
        context['form_url'] = reverse('add_module')
        context['form_title'] = '创建模块'
        return context


class ModuleUpdateView(UpdateView):
    model = Module
    template_name = 'manage/form/create_form.html'
    form_class = ModuleForm
    success_url = 'modules'

    def get_context_data(self, **kwargs):
        context = super(ModuleUpdateView, self).get_context_data(**kwargs)
        context['form_url'] = reverse('edit_module', kwargs={'pk': self.kwargs.get(self.pk_url_kwarg)})
        context['form_title'] = '编辑模块'
        return context

    def form_valid(self, form):
        if form.is_valid:
            form.save()
            return HttpResponseRedirect(reverse(self.success_url))


class FieldListView(ListView):
    template_name = 'manage/system/module_field_list.html'
    context_object_name = "data"
    paginate_by = 20

    def post(self, request, **kwargs):
        sort_id = request.POST.get('sort_id', None)
        data = {}
        if sort_id:
            sort_value = request.POST.get('sort_value', 0)
            ModuleField.objects.filter(id=sort_id).update(sort=sort_value)
            data['success'] = 1
        else:
            id_list = request.POST.getlist('id_list[]')

            if id_list:
                idstring = ','.join(id_list)
                ModuleField.objects.extra(where=['id IN (' + idstring + ')']).delete()
                FieldItem.objects.extra(where=['field_id IN (' + idstring + ')']).delete()
                data['success'] = 1
            else:
                data['success'] = 0

        return HttpResponse(json.dumps(data), content_type="application/json")

    def get_queryset(self):
        module_id = self.kwargs.get('mid')
        listdata = ModuleField.objects.filter(module_id=module_id).order_by('sort', 'id')
        keyword = self.request.GET.get('q')
        if keyword:
            listdata = listdata.filter(Q(name__icontains=keyword) | Q(title__icontains=keyword))
        return listdata

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(FieldListView, self).get_context_data(**kwargs)
        context['module_id'] = self.kwargs.get('mid')
        context['form_url'] = reverse('fields', kwargs={'mid': context['module_id']})
        context['q'] = self.request.GET.get('q', '')
        return context


class FieldCreateView(CreateView):
    form_class = ModuleFieldForm
    template_name = 'manage/form/create_form.html'
    success_url = 'fields'

    def get_form_kwargs(self):
        kw = super(FieldCreateView, self).get_form_kwargs()
        kw.update({
            'module_id': self.kwargs.get('mid')
        })
        return kw

    def form_valid(self, form):
        if form.is_valid:
            form.save()
            return HttpResponseRedirect(reverse(self.success_url, kwargs={'mid': self.kwargs.get('mid')}))

    def get_context_data(self, **kwargs):
        context = super(FieldCreateView, self).get_context_data(**kwargs)
        context['module_id'] = self.kwargs.get('mid')
        context['form_url'] = reverse('add_field', kwargs={'mid': context['module_id']})
        context['form_title'] = '添加自定义字段'
        return context


class FieldUpdateView(UpdateView):
    model = ModuleField
    form_class = ModuleFieldForm
    template_name = 'manage/form/create_form.html'
    success_url = 'fields'

    def get_context_data(self, **kwargs):
        context = super(FieldUpdateView, self).get_context_data(**kwargs)
        context['form_url'] = reverse('edit_field', kwargs={'pk': self.kwargs.get(self.pk_url_kwarg)})
        context['form_title'] = '编辑自定义字段'
        return context

    def form_valid(self, form):
        if form.is_valid:
            form.save()
            return HttpResponseRedirect(reverse(self.success_url, kwargs={'mid': form.data.get('module_id')}))

        return super(FieldUpdateView, self).form_valid(form)
