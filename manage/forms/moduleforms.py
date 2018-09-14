import os
from DjangoUeditor.widgets import UEditorWidget
from django import forms
from  DjangoUeditor.forms import UEditorField
from manage.models import Module
from manage.models import Article
from manage.models import ArticleContent
from manage.models import Category
from manage.models import ModuleField
from manage.models import FieldItem
from manage.utils import TreeUtil
from manage.utils import FieldUtil
from manage.utils import ModuleUtil
from manage.utils import CategoryUtil
import json
from PIL import Image
from django.conf import settings

class ArticleForm(forms.ModelForm):
    extraFields = {}

    def createField(self, field=None):
        if field['type'] == 'text':
            self.fields[field['name']] = forms.CharField(
                label=field['title'],
                max_length=int(field['length']),
                widget=forms.TextInput(
                    attrs={'class': 'form-control'}
                )

            )

    def saveField(self, article_id):
        if article_id:
            content = ArticleContent(id=article_id, content=self.cleaned_data['content'])
            content.save()
            if len(self.extraFields):
                for field in self.extraFields:
                    model = FieldItem()
                    model.module_id = field['module_id']
                    model.field_id = field['id']
                    model.object_id = article_id
                    model.content = self.cleaned_data[field['name']]
                    model.save()

    def cropImg(self, filename):
        # filename = settings.MEDIA_ROOT+"/"+filename
        try:
            with Image.open(filename) as im:
                size = (300, 300)
                im.thumbnail(size)
                im.save(filename+'_thumnail.jpg')
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
        extra_data = kwargs.pop('extra_data', None)
        super(ArticleForm, self).__init__(*args, **kwargs)
        module_name = 'article'
        module_id = ModuleUtil.getModuleId(module_name)

        '''分类下拉列表'''
        self.fields['cat_id'] = forms.ChoiceField(label=u'文章分类', widget=forms.Select(attrs={'class': 'form-control'}))
        trees = CategoryUtil.getCategoryTree(module_id, 0, '|', '')
        # trees = [('0', '顶级分类')] + trees
        self.fields['cat_id'].choices = trees

        self.fields['cover'] = forms.ImageField(label=u'封面',)

        '''文章内容'''
        # self.fields['content'] = forms.CharField(label=u'内容', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 20}))
        self.fields['content'] = forms.CharField(label=u'内容', widget=UEditorWidget(
            attrs={'width': '100%', 'height': 400,'imagePath': 'upload/images/', 'filePath': 'upload/files/', 'toolbars': [[
                'fullscreen', 'source', '|', 'undo', 'redo', '|', 'bold', 'italic', 'underline', 'fontborder', 'strikethrough',
                'superscript', 'subscript', 'removeformat', 'formatmatch', 'autotypeset', 'blockquote', 'pasteplain', '|',
                'forecolor', 'backcolor', 'insertorderedlist', 'insertunorderedlist', 'selectall', '|',
                'simpleupload', 'insertimage', 'emotion', 'insertvideo', 'music', 'attachment', 'map', 'gmap',
                'insertcode', 'webapp', 'pagebreak',  'template', '|', 'selectall', 'cleardoc'
        ]]}
        ))

        '''自定义字段处理'''
        self.extraFields = FieldUtil.getModuleFields(extra_data['id']).values()
        if len(self.extraFields):
            for field in self.extraFields:
                self.createField(field)

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

class ModuleItemForm(forms.Form):
    # full_name = forms.CharField(help_text="Full Name")

    def createField(self, field=None):
        if field['type'] == 'text':
            self.fields[field['name']] = forms.CharField(
                label=field['title'],
                max_length=int(field['length']),
                widget=forms.TextInput(
                    attrs={'class': 'form-control'}
                )

            )


    def __init__(self, *args, **kwargs):
        data = kwargs.pop('data', None)
        super(ModuleItemForm, self).__init__(*args, **kwargs)
        itemFields = FieldUtil.getModuleFields(data['id']).values()
        if len(itemFields):
            for field in itemFields:
                self.createField(field)


