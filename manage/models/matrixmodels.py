from django.utils import timezone

from .basemodel import *


class BaseMatrixModel(BaseModel):

    @property
    def id(self):
        raise NotImplementedError("field id is not exists.")

    @property
    def title(self):
        raise NotImplementedError("field title is not exists.")

    @property
    def sort(self):
        raise NotImplementedError("field sort is not exists.")

    @staticmethod
    def list_fields():
        raise NotImplementedError("list_fields is not implemented.")

    class Meta:
        app_label = 'manage'
        abstract = True


class Article(BaseMatrixModel):

    @staticmethod
    def list_fields():
        return ['id', 'cat_id', 'title', 'sort', 'status',  'create_time']

    id = models.BigAutoField(primary_key=True)
    cat_id = models.IntegerField(u"分类ID")
    title = models.CharField(u"标题", max_length=100, error_messages={'required': u'请输入标题', 'max_length': u'标题最长为100个字符'})
    desc = models.CharField(u"简介", max_length=255, error_messages={'required': u'请输入简介', 'max_length': u'简介最长为200个字符'})
    user_id = models.BigIntegerField(u"用户ID", default=0)
    author = models.CharField(u"作者", max_length=20, blank=True)
    source = models.CharField(u"来源", max_length=200, blank=True)
    status = models.SmallIntegerField(u"状态", default=0)
    cover = models.FileField(u"封面图", blank=True)
    pub_time = models.DateTimeField(u"发表时间", default=timezone.now)
    create_time = models.DateTimeField(u"创建时间", default=timezone.now)
    update_time = models.DateTimeField(u"更新时间", auto_now=True)
    sort = models.IntegerField(u"排序", blank=True, default=0)

    class Meta(BaseModel.Meta):
        db_table = 'article'
        verbose_name = '文章'
        verbose_name_plural = '文章列表'


class ArticleContent(BaseModel):
    id = models.BigIntegerField(primary_key=True)
    content = models.TextField(u"内容")

    class Meta(BaseModel.Meta):
        db_table = 'article_content'
        verbose_name = '内容'
        verbose_name_plural = '内容列表'