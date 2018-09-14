from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.base import View
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.urls import reverse
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
import json

from manage.models import Module
from manage.models import Category
from manage.models import ModuleField
from manage.forms import ModuleAddForm
from manage.forms import ModuleUpdateForm
from manage.forms import ModuleFieldForm
from manage.forms import ModuleItemForm
from manage.forms import ArticleForm
from manage.utils import TreeUtil
from manage.utils import FieldUtil
from manage.utils import ModuleUtil

from django.shortcuts import render

class ItemCreateView(View):

    def get(self, request, *args, **kwargs):
        context = {}
        modules = ModuleUtil.getModules()
        module_name = self.kwargs.get('module_name')
        module = modules[module_name]
        # fields = FieldUtil.getModuleFields(module['id'])
        form = ModuleItemForm(data=module)
        context['form'] = form
        context['form_url'] = reverse('add_item', kwargs={'module_name': module_name})
        context['form_title'] = '添加' + module.get('title')

        return render(request, 'manage/system/create_form.html', context)

class ArticleCreateView(CreateView):
    form_class = ArticleForm
    template_name = 'manage/system/create_form.html'
    success_url = 'add_article'

    def get_form_kwargs(self):
        kw = super(ArticleCreateView, self).get_form_kwargs()
        modules = ModuleUtil.getModules()
        module = modules['article']
        kw.update({
            'extra_data': module
        })
        return kw

    def form_valid(self, form):
        if form.is_valid:
            form.save()

            return HttpResponseRedirect(reverse(self.success_url))

    def get_context_data(self, **kwargs):
        context = super(ArticleCreateView, self).get_context_data(**kwargs)
        context['form_url'] = reverse('add_article')
        context['form_title'] = '添加文章'
        return context
