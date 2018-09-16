from manage.models import Module


class ModuleUtil(object):

    @staticmethod
    def getMatrixs():
        return {'article': '文章', 'product': '商品'}

    @staticmethod
    def matrixIsExists(matrix):
        return True if ModuleUtil.getMatrixs().get(matrix, None) else False

    @staticmethod
    def getModules():
        result = Module.objects.all().values()
        modules = {}
        if len(result):
            for mod in result:
                modules[mod['name']] = mod

        return modules

    @staticmethod
    def getModuleId(module_name):
        return getattr(Module.objects.get(name=module_name), 'id', 0) if module_name else 0
