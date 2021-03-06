import operator

from manage.models import ModuleField, FieldItem

from django.apps import apps

class FieldUtil(object):

    FIELD_TEXT = 'text'
    FIELD_TEXTAREA = 'textarea'
    FIELD_EDITOR = 'editor'
    FIELD_NUMBER = 'number'
    FIELD_SELECT = 'select'
    FIELD_SELECTMULTIPLE = 'select_multiple'
    FIELD_CHECKBOX = 'checkbox'
    FIELD_RADIO = 'radio'
    FIELD_IMAGE = 'image'
    FIELD_FILE = 'file'
    FIELD_DATETIME = 'datetime'
    FIELD_DATE = 'date'
    FIELD_TIME = 'time'
    FIELD_EMAIL = 'email'
    FIELD_DECIMAL = 'decimal'
    FIELD_FLOAT = 'float'

    FieldType = {
        FIELD_TEXT: u'文本',
        FIELD_TEXTAREA: u'文本域',
        FIELD_EDITOR: u'编辑器',
        FIELD_NUMBER: u'数值',
        FIELD_SELECT: u'选项',
        # FIELD_SELECTMULTIPLE: u'多项选择',
        FIELD_CHECKBOX: u'复选框',
        FIELD_RADIO: u'单选框',
        FIELD_IMAGE: u'图片',
        FIELD_FILE: u'文件',
        FIELD_DATETIME: u'日期时间',
        FIELD_DATE: u'日期',
        FIELD_TIME: u'时间',
        FIELD_EMAIL: u'邮箱',
        FIELD_DECIMAL: u'金额',
        FIELD_FLOAT: u'小数'
    }

    @staticmethod
    def getFieldOptions():
        fields = FieldUtil.FieldType
        return tuple(fields.items())

    @staticmethod
    def getModuleFields(module_id):
        fields = ModuleField.objects.filter(module_id=module_id).order_by('sort', 'id')
        return fields

    @staticmethod
    def getOptions(tr_str):
        optstr = str(tr_str)
        options = []
        if optstr.strip():
            tmparr = optstr.splitlines()
            filter(None, tmparr)
            for item in tmparr:
                options.append(item.split('=', 1))
        return options

    @staticmethod
    def getmodelfields(model, use_fields):
        _fileds = model._meta.fields
        fileds = {}
        if use_fields:
            params = [f for f in _fileds if f.name in use_fields]
        else:
            params = [f for f in _fileds]
        for i in params:
            fileds[i.name] = i.verbose_name
        return fileds

    @staticmethod
    def getItems(module_id, object_id):
        items = {}
        result = FieldItem.objects.filter(module_id=module_id, object_id=object_id).values()

        for item in result:
            items[item['field_id']] = item

        return items

