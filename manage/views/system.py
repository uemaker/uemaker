from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.shortcuts import render
from manage.models import Module
from manage.forms import ModuleAddForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q
import json
from django.http import HttpResponse

class IndexView(TemplateView):

    template_name = 'manage/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        return context

class ModuleListView(ListView):
    # model = Module
    template_name = 'manage/system/module_list.html'
    context_object_name = "modules"
    paginate_by = 2

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

def module_add(request):
    context = {}
    context['form_url'] = reverse('add_module')
    context['form_title'] = '创建模块'

    if request.method == 'POST':
        form = ModuleAddForm(request.POST)
        context['form'] = form
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/manage/system/modules/")
        else:
            return render(request, 'manage/system/module_add.html', context)

    context['form'] = ModuleAddForm()
    return render(request, 'manage/system/module_add.html', context)

def module_edit(request, id):
    context = {}
    context['id'] = id
    context['form_url'] = reverse('edit_module', args=[id])
    context['form_title'] = '编辑模块'
    model = Module.objects.filter(id=id).first()

    if request.method == 'POST':
        form = ModuleAddForm(request.POST, instance=model)
        context['form'] = form
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(context['form_url'])
        else:
            return render(request, 'manage/system/module_add.html', context)

    form = ModuleAddForm(instance=model)
    context['form'] = form
    return render(request, 'manage/system/module_add.html', context)

