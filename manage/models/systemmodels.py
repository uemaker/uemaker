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