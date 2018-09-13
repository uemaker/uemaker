from manage.models import ModuleField

class FieldUtil(object):

    FieldType = {
        'text': u'文本',
        'number': u'数值',
        'select': u'选项',
        'checkbox': u'复选框',
        'radio': u'单选框',
        'image': u'图片',
        'datetime': u'日期时间',
        'date': u'日期',
        'time': u'时间',
        'email': u'邮箱',
        'decimal': u'金额'
    }

    @staticmethod
    def getFieldOptions():
        fields = FieldUtil.FieldType
        return tuple(fields.items())

    @staticmethod
    def getModuleFields(module_id):
        fields = ModuleField.objects.filter(module_id=module_id)
        return fields
