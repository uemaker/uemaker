from .basemodel import *


class Module(BaseModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(u"模块标识", max_length=20, unique=True, error_messages={'required': u'请填写标识', 'unique': u'标识名已存在', 'max_length': u'标识最长为20个字符'})
    title = models.CharField(u"模块名称", max_length=20)
    matrix = models.CharField(u"模型", max_length=20, blank=True)
    is_system = models.BooleanField(u"系统模块", default=False)
    desc = models.CharField(u"模块介绍", max_length=200, blank=True)
    config = models.CharField(u"配置", max_length=255, blank=True)

    class Meta(BaseModel.Meta):
        db_table = 'module'
        verbose_name = '模块'
        verbose_name_plural = '模块列表'

class ModuleField(BaseModel):
    id = models.AutoField(primary_key=True)
    module_id = models.IntegerField(u"模块ID")
    type = models.CharField(u"字段类型", max_length=20)
    name = models.CharField(u"字段名称", max_length=20, error_messages={'required': u'请输入标识', 'max_length': u'标识最长为20个字符'})
    title = models.CharField(u"字段说明", max_length=20, error_messages={'required': u'请输入名称', 'max_length': u'名称最长为20个字符'})
    length = models.SmallIntegerField(u"字段长度")
    blank = models.BooleanField(u"是否必填", blank=True, default=True)
    default = models.CharField(u"默认值", max_length=100, blank=True)
    help_text = models.CharField(u"帮助提示", max_length=100, blank=True)
    value = models.CharField(u"选项", max_length=200, blank=True)
    sort = models.IntegerField(u"排序",  blank=True, default=0)

    class Meta(BaseModel.Meta):
        db_table = 'module_field'
        verbose_name = '模块字段'
        verbose_name_plural = '模块字段列表'

class FieldItem(BaseModel):
    id = models.BigAutoField(primary_key=True)
    module_id = models.IntegerField("模块ID")
    field_id = models.IntegerField(u"字段ID")
    object_id = models.BigIntegerField("模型对象ID")
    content = models.CharField(u"字段内容", max_length=255)

    class Meta(BaseModel.Meta):
        db_table = 'field_item'
        verbose_name = '字段内容'
        verbose_name_plural = '字段内容列表'

class Category(BaseModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(u"英文名称", max_length=20, unique=True, error_messages={'required': u'请输入英文名称', 'unique': u'英文名称已存在', 'max_length': u'英文名称最长为20个字符'})
    title = models.CharField(u"中文名称", max_length=20, error_messages={'required': u'请输入中文名称', 'max_length': u'中文名称最长为20个字符'})
    pid = models.IntegerField(u"上级分类", default=0)
    path = models.CharField(u"路径", max_length=255, blank=True, default='')
    module_id = models.IntegerField(u"模块ID", default=0)
    config = models.CharField(u"配置信息", max_length=255, blank=True, default='')
    sort = models.IntegerField(u"排序", default=0)

    class Meta(BaseModel.Meta):
        db_table = 'category'
        verbose_name = '分类'
        verbose_name_plural = '分类列表'
