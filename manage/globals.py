from .utils import ModuleUtil


def settings(request):
    context = {
        'G_MODULES': ModuleUtil.getModules(),
        'G_MODULE_URL_PREFIX': '/manage/module/'
    }
    return context
