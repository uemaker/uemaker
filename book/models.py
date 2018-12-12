from django.db import models

# Create your models here.


class Book(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(u"书籍名称", max_length=50, unique=True, error_messages={'required': u'请填写书籍名称', 'unique': u'书籍名称已存在', 'max_length': u'书籍名称最长为50个字符'})
    title = models.CharField(u"书籍英文名称", max_length=20)
    desc = models.CharField(u"书籍介绍", max_length=1000, blank=True)

    class Meta:
        db_table = 'book'
        verbose_name = u'书籍'
        verbose_name_plural = u'书籍列表'


class Chapter(models.Model):
    id = models.BigAutoField(primary_key=True)
    code = models.CharField(u"章节编号", max_length=20, default='', blank=True)
    title = models.CharField(u"章节标题", max_length=100, error_messages={'required': u'请输入标题', 'max_length': u'标题最长为100个字符'})
    pid = models.IntegerField(u"父级ID", default=0)
    path = models.CharField(u"路径", max_length=255, blank=True, default='')
    book_id = models.IntegerField(u"书籍ID", default=0)
    content = models.TextField(u"章节内容", default='', blank=True)
    sort = models.IntegerField(u"排序", default=0)

    class Meta:
        db_table = 'book_chapter'
        verbose_name = u'章节'
        verbose_name_plural = u'章节列表'

