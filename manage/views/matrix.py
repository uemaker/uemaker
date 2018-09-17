import importlib

from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.views.generic import CreateView, ListView
from django.apps import apps

from manage.forms import *
from manage.utils import StrUtil


class MatrixListView(ListView):
    template_name = 'manage/matrix/matrix_list.html'
    context_object_name = "data"
    paginate_by = 20

    def get_queryset(self, *args, **kwargs):
        module_name = self.kwargs.get('module_name')
        module_id = ModuleUtil.getModuleId(module_name)
        matrix = ''
        if module_id:
            matrix = Module.objects.only('matrix').get(id=module_id).matrix
        if not matrix or not ModuleUtil.matrixIsExists(matrix):
            raise Http404()
        model_class_name = StrUtil.ucwords(matrix)
        model = apps.get_model('manage', model_class_name)
        fileds = FieldUtil.getmodelfields(model, model.list_fields())
        self.extra_context = {'fields': fileds}
        # print(fileds.items())
        data = model.objects.filter().order_by('sort', 'id')
        keyword = self.request.GET.get('q')
        if keyword:
            data = data.filter(title__icontains=keyword)

        return data

    def get_context_data(self, **kwargs):
        context = super(MatrixListView, self).get_context_data(**kwargs)
        context['module_name'] = self.kwargs.get('module_name')
        context['form_url'] = reverse('add_matrix', kwargs={'module_name': context['module_name']})
        context['form_title'] = '添加'
        return context

class MatrixCreateView(CreateView):
    template_name = 'manage/form/create_form.html'
    success_url = 'matrix'

    def get_form_class(self):
        module_name = self.kwargs.get('module_name')
        module_id = ModuleUtil.getModuleId(module_name)
        matrix = ''
        if module_id:
            matrix = Module.objects.only('matrix').get(id=module_id).matrix
        if not matrix or not ModuleUtil.matrixIsExists(matrix):
            raise Http404()
        form_class_name = StrUtil.ucwords(matrix) + 'Form'
        matrixforms = importlib.import_module('manage.forms.matrixforms')
        self.form_class = getattr(matrixforms, form_class_name)
        return super(MatrixCreateView, self).get_form_class()

    def get_form_kwargs(self):
        kw = super(MatrixCreateView, self).get_form_kwargs()
        module_name = self.kwargs.get('module_name')
        module = ModuleUtil.getModules().get(module_name)
        kw.update({
            'module': module
        })
        return kw

    def form_valid(self, form):
        if form.is_valid:
            form.save()
            return HttpResponseRedirect(reverse(self.success_url, kwargs={'module_name': self.kwargs.get('module_name')}))
        return super(MatrixCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(MatrixCreateView, self).get_context_data(**kwargs)
        context['module_name'] = self.kwargs.get('module_name')
        context['form_url'] = reverse('add_matrix', kwargs={'module_name': context['module_name']})
        context['form_title'] = '添加文章'
        return context