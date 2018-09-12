from .basemodel import *

class Module(BaseModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(u"模块标识", max_length=20, unique=True, error_messages={'required': u'请填写标识', 'unique': u'标识名已存在', 'max_length': u'标识最长为20个字符'})
    title = models.CharField(u"模块名称", max_length=20)
    is_system = models.BooleanField(u"系统模块", default=False)
    sort = models.IntegerField(u"排序")

    class Meta(BaseModel.Meta):
        db_table = 'module'
        verbose_name = '模块'
        verbose_name_plural = '模块列表'

class Category(BaseModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(u"英文名称", max_length=20, unique=True, error_messages={'required': u'请填写英文名称', 'unique': u'英文名称已存在', 'max_length': u'英文名称最长为20个字符'})
    title = models.CharField(u"中文名称", max_length=20, error_messages={'required': u'请填写中文名称', 'max_length': u'中文名称最长为20个字符'})
    pid = models.IntegerField(u"上级分类", default=0)
    path = models.CharField(u"路径", max_length=255, blank=True, default='')
    # module_id = models.IntegerField(u"所属模块")
    module = models.ForeignKey(Module, related_name='module', on_delete=models.CASCADE)
    config = models.CharField(u"配置信息", max_length=255, blank=True, default='')
    sort = models.IntegerField(u"排序", default=0)

    class Meta(BaseModel.Meta):
        db_table = 'category'
        verbose_name = '分类'
        verbose_name_plural = '分类列表'

    def __str__(self):
        return self.module
