import datetime
import os
import random

from PIL import Image
from django.conf import settings

from manage.models import FieldItem, Article, ArticleContent
from manage.utils import CategoryUtil
from .baseform import *


class ArticleForm(BaseModelForm):
    extra_fields = {}

    def saveField(self, article_id):
        if article_id:
            content = ArticleContent(id=article_id, content=self.cleaned_data['content'])
            content.save()
            if len(self.extra_fields):
                for field in self.extra_fields:
                    if field['type'] == FieldUtil.FIELD_IMAGE or field['type'] == FieldUtil.FIELD_FILE:
                        ext_name = os.path.splitext(self.cleaned_data[field['name']].name)[1]
                        nowTime = datetime.now().strftime("%Y%m%d%H%M%S")  # 生成当前的时间
                        randomNum = random.randint(0, 100)
                        fname = 'field_%s%d%s' % (nowTime, randomNum, ext_name)
                        f = open(os.path.join(settings.MEDIA_ROOT, 'upload', fname), 'wb')
                        for line in self.cleaned_data[field['name']].chunks():
                            f.write(line)
                        f.close()
                        field_name = fname
                    else:
                        field_name = self.cleaned_data[field['name']]

                    model = FieldItem()
                    model.module_id = field['module_id']
                    model.field_id = field['id']
                    model.object_id = article_id
                    model.content = field_name
                    model.save()

    def cropImg(self, filename):
        # filename = settings.MEDIA_ROOT+"/"+filename
        try:
            with Image.open(filename) as im:
                size = (300, 300)
                im.thumbnail(size)
                im.save(filename + '_thumnail.jpg')
        except OSError as e:
            print(e)

    class Meta:
        model = Article
        fields = ['cat_id', 'title', 'desc', 'author', 'source', 'cover']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'desc': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'source': forms.TextInput(attrs={'class': 'form-control'}),
            # 'cover': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        module = kwargs.pop('module', None)
        super(ArticleForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        is_update = True if instance and instance.pk else False
        module_name = module.get('name')
        module_id = module.get('id')

        '''分类下拉列表'''
        self.fields['cat_id'] = forms.ChoiceField(label=u'文章分类', widget=forms.Select(attrs={'class': 'form-control'}))
        trees = CategoryUtil.getCategoryTree(module_id, 0, '|', '')
        # trees = [('0', '顶级分类')] + trees
        self.fields['cat_id'].choices = trees

        self.fields['cover'] = forms.ImageField(label=u'封面', required=False)

        '''文章内容'''
        content = ''
        extra_items = {}
        if is_update:
            content = ArticleContent.objects.only('content').get(id=instance.id).content
            extra_items = FieldUtil.getItems(module_id, instance.id)

        # self.fields['content'] = forms.CharField(label=u'内容', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 20}))
        self.fields['content'] = forms.CharField(label=u'内容', initial=content, widget=UEditorWidget(
            attrs={'width': '100%', 'height': 400, 'imagePath': 'upload/images/', 'filePath': 'upload/files/',
                   'toolbars': [[
                       'fullscreen', 'source', '|', 'undo', 'redo', '|', 'bold', 'italic', 'underline', 'fontborder',
                       'strikethrough',
                       'superscript', 'subscript', 'removeformat', 'formatmatch', 'autotypeset', 'blockquote',
                       'pasteplain', '|',
                       'forecolor', 'backcolor', 'insertorderedlist', 'insertunorderedlist', 'selectall', '|',
                       'simpleupload', 'insertimage', 'emotion', 'insertvideo', 'music', 'attachment', 'map', 'gmap',
                       'insertcode', 'webapp', 'pagebreak', 'template', '|', 'selectall', 'cleardoc'
                   ]]},
        ))

        '''自定义字段处理'''
        self.extra_fields = FieldUtil.getModuleFields(module_id).values()
        if len(self.extra_fields):
            for field in self.extra_fields:
                extra_item = extra_items.get(field.get('id')) if extra_items else None
                extra_val = extra_item.get('content') if extra_item else None
                self.createField(field, extra_val, is_update)

    def clean(self):
        is_insert = self.instance.pk is None

        return self.cleaned_data

    def save(self, commit=True):
        media = super(ArticleForm, self).save(commit=False)
        if commit:
            media.save()
            if media.id:
                self.saveField(media.id)
            # if media.cover:
            #     self.cropImg(os.path.abspath(media.cover))
