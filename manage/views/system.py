from django.views.generic.base import View
from django.views.generic.list import ListView
from django.shortcuts import render
from manage.models import Module
from manage.forms import ModuleAddForm
from django.http import HttpResponseRedirect
from django.urls import reverse

class IndexView(View):

    def get(self, request):
        return render(request, 'manage/index.html', {})

class ModuleListView(ListView):
    model = Module
    context_object_name = "modules"
    template_name = 'manage/system/module_list.html'
    paginate_by = 2

def module_add(request):
    context = {}
    context['form_url'] = reverse('add_module')

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

