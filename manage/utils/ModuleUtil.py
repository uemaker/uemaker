from manage.models import Module
import json
from django.forms.models import model_to_dict

class ModuleUtil(object):

    @staticmethod
    def getModules():
        result = Module.objects.all().values()
        modules = {}
        if len(result):
            for mod in result:
                modules[mod['name']] = mod

        return modules
