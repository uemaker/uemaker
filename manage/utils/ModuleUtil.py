from manage.models import Module, Category


class ModuleUtil(object):

    @staticmethod
    def getMatrixs():
        return {'article': '文章', 'product': '商品', 'picture': '图片'}

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

    @staticmethod
    def getModuleIdByCatId(cat_id):
        return Category.objects.only('module_id').get(id=cat_id).module_id
