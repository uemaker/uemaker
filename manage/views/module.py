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
from manage.utils import TreeUtil
from manage.utils import FieldUtil
from manage.utils import ModuleUtil

from django.shortcuts import render

class ItemCreateView(View):

    def get(self, request, *args, **kwargs):
        modules = ModuleUtil.getModules()
        module_name = self.kwargs.get('module_name')
        module = modules[module_name]
        # fields = FieldUtil.getModuleFields(module['id'])
        form = ModuleItemForm(data=module)

        return render(request, 'manage/index.html', {'form': form})




