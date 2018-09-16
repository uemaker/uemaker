import json

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.urls import reverse
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView

from manage.forms import CategoryForm
from manage.models import Category
from manage.utils import ModuleUtil, CategoryUtil


class CategoryListView(ListView):
    template_name = 'manage/module/category_list.html'
    context_object_name = "data"
    paginate_by = 100

    def post(self, request, *args, **kwargs):
        sort_id = request.POST.get('sort_id', None)
        data = {}
        if sort_id:
            sort_value = request.POST.get('sort_value', 0)
            Category.objects.filter(id=sort_id).update(sort=sort_value)
            data['success'] = 1
        else:
            cat_id = request.POST.get('id')
            if cat_id:
                Category.objects.get(id=cat_id).delete()
                data['success'] = 1
            else:
                data['success'] = 0

        return HttpResponse(json.dumps(data), content_type="application/json")

    def get_queryset(self, *args, **kwargs):
        module_name = self.kwargs.get('module_name', None)
        module_id = ModuleUtil.getModuleId(module_name)
        data = {}
        if module_id:
            data = CategoryUtil.getCategoryList(module_id, 0, 0)

        if not module_id:
            raise Http404()

        return data

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        context['module_name'] = self.kwargs.get('module_name', None)
        context['form_url'] = reverse('category', kwargs={'module_name': context['module_name']})
        return context


class CategoryCreateView(CreateView):
    form_class = CategoryForm
    template_name = 'manage/form/create_form.html'
    pid = 0
    success_url = 'category'

    def form_valid(self, form):
        if form.is_valid:
            form.save()
            return HttpResponseRedirect(reverse(self.success_url, kwargs={'module_name': self.kwargs.get('module_name')}))
        return super(CategoryCreateView, self).form_valid(form)

    def get_initial(self):
        initial = super(CategoryCreateView, self).get_initial()
        self.pid = self.request.GET.get('pid', 0)
        return initial

    def get_form_kwargs(self):
        kw = super(CategoryCreateView, self).get_form_kwargs()
        kw.update({
            'pid': self.pid,
            'module_name': self.kwargs.get('module_name')
        })
        return kw

    def get_context_data(self, **kwargs):
        context = super(CategoryCreateView, self).get_context_data(**kwargs)
        context['module_name'] = self.kwargs.get('module_name')
        context['form_url'] = reverse('add_category', kwargs={'module_name': context['module_name']})
        context['form_title'] = '创建分类'
        return context


class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'manage/form/create_form.html'
    success_url = 'category'

    def form_valid(self, form):
        if form.is_valid:
            form.save()
            return HttpResponseRedirect(reverse(self.success_url, kwargs={'module_name': self.kwargs.get('module_name')}))

        return super(CategoryUpdateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CategoryUpdateView, self).get_context_data(**kwargs)
        context['module_name'] = self.kwargs.get('module_name')
        context['form_url'] = reverse('edit_category', kwargs={'module_name': context['module_name'], 'pk': self.kwargs.get(self.pk_url_kwarg)})
        context['form_title'] = '编辑分类'
        return context
