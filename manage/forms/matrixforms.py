import datetime
import decimal
import os
import random

from DjangoUeditor.widgets import UEditorWidget
from PIL import Image
from django import forms
from django.conf import settings

from manage.models import FieldItem, Article, ArticleContent
from manage.utils import FieldUtil, ModuleUtil, CategoryUtil


class ArticleForm(forms.ModelForm):
    extraFields = {}

    def createField(self, field=None):
        print(field)
        blank = field['blank']
        if field['type'] == FieldUtil.FIELD_TEXT:
            self.fields[field['name']] = forms.CharField(
                label=field['title'],
                max_length=int(field['length']),
                required=blank,
                initial=field['default'],
                help_text=field['help_text'],
                widget=forms.TextInput(
                    attrs={'class': 'form-control'},
                )
            )
        elif field['type'] == FieldUtil.FIELD_TEXTAREA:
            self.fields[field['name']] = forms.CharField(
                label=field['title'],
                max_length=int(field['length']),
                required=blank,
                initial=field['default'],
                help_text=field['help_text'],
                widget=forms.Textarea(
                    attrs={'class': 'form-control'},
                )

            )
        elif field['type'] == FieldUtil.FIELD_EDITOR:
            self.fields[field['name']] = forms.CharField(
                label=field['title'],
                max_length=int(field['length']),
                required=blank,
                initial=field['default'],
                help_text=field['help_text'],
                widget=UEditorWidget(
                    attrs={'width': '100%', 'height': 400, 'imagePath': 'upload/images/', 'filePath': 'upload/files/',
                           'toolbars': [
                               ['fullscreen', 'source', '|', 'undo', 'redo', '|', 'bold', 'italic', 'underline',
                                'fontborder', 'strikethrough',
                                'superscript', 'subscript', 'removeformat', 'formatmatch', 'autotypeset', 'blockquote',
                                'pasteplain', '|',
                                'forecolor', 'backcolor', 'insertorderedlist', 'insertunorderedlist', 'selectall', '|',
                                'simpleupload', 'insertimage', 'emotion', 'insertvideo', 'music', 'attachment', 'map',
                                'gmap',
                                'insertcode', 'webapp', 'pagebreak', 'template', '|', 'selectall', 'cleardoc']]
                           })
            )
        elif field['type'] == FieldUtil.FIELD_NUMBER:
            self.fields[field['name']] = forms.CharField(
                label=field['title'],
                max_length=int(field['length']),
                required=blank,
                initial=int(field['default']),
                help_text=field['help_text'],
                widget=forms.NumberInput(
                    attrs={'class': 'form-control'},
                )

            )
        elif field['type'] == FieldUtil.FIELD_SELECT:
            self.fields[field['name']] = forms.ChoiceField(
                label=field['title'],
                required=blank,
                initial=field['default'],
                help_text=field['help_text'],
                widget=forms.Select(
                    attrs={'class': 'form-control'},
                )
            )
            self.fields[field['name']].choices = FieldUtil.getOptions(field['value'])
        elif field['type'] == FieldUtil.FIELD_CHECKBOX:
            self.fields[field['name']] = forms.BooleanField(
                label=field['title'],
                required=blank,
                initial=field['default'],
                help_text=field['help_text'],
                widget=forms.CheckboxInput(
                )

            )
        elif field['type'] == FieldUtil.FIELD_RADIO:
            self.fields[field['name']] = forms.BooleanField(
                label=field['title'],
                required=blank,
                initial=int(field['default']),
                help_text=field['help_text'],
                widget=forms.RadioSelect(
                    attrs={},
                )

            )
        elif field['type'] == FieldUtil.FIELD_IMAGE:
            self.fields[field['name']] = forms.ImageField(
                label=field['title'],
                required=blank,
                help_text=field['help_text'],
            )
        elif field['type'] == FieldUtil.FIELD_FILE:
            self.fields[field['name']] = forms.FileField(
                label=field['title'],
                required=blank,
                help_text=field['help_text'],
            )
        elif field['type'] == FieldUtil.FIELD_DATETIME:
            self.fields[field['name']] = forms.DateTimeField(
                label=field['title'],
                required=blank,
                help_text=field['help_text'],
            )
        elif field['type'] == FieldUtil.FIELD_DATE:
            self.fields[field['name']] = forms.DateField(
                label=field['title'],
                required=blank,
                help_text=field['help_text'],
            )
        elif field['type'] == FieldUtil.FIELD_TIME:
            self.fields[field['name']] = forms.TimeField(
                label=field['title'],
                required=blank,
                help_text=field['help_text'],
            )
        elif field['type'] == FieldUtil.FIELD_EMAIL:
            self.fields[field['name']] = forms.EmailField(
                label=field['title'],
                required=blank,
                help_text=field['help_text'],
                initial=field['default'],
                widget=forms.ClearableFileInput(
                    attrs={'class': 'form-control'},
                )
            )
        elif field['type'] == FieldUtil.FIELD_DECIMAL:
            default = field['default'] if decimal.Decimal(field['default']) else None
            self.fields[field['name']] = forms.DecimalField(
                label=field['title'],
                required=blank,
                help_text=field['help_text'],
                initial=default,
                widget=forms.NumberInput(
                    attrs={'class': 'form-control'},
                )
            )
        elif field['type'] == FieldUtil.FIELD_FLOAT:
            default = field['default'] if float(field['default']) else None
            self.fields[field['name']] = forms.FloatField(
                label=field['title'],
                required=blank,
                help_text=default,
                initial=float(field['default']),
                widget=forms.NumberInput(
                    attrs={'class': 'form-control'},
                )
            )

    def saveField(self, article_id):
        if article_id:
            content = ArticleContent(id=article_id, content=self.cleaned_data['content'])
            content.save()
            if len(self.extraFields):
                for field in self.extraFields:
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
        extra_data = kwargs.pop('extra_data', None)
        super(ArticleForm, self).__init__(*args, **kwargs)
        module_name = 'article'
        module_id = ModuleUtil.getModuleId(module_name)

        '''分类下拉列表'''
        self.fields['cat_id'] = forms.ChoiceField(label=u'文章分类', widget=forms.Select(attrs={'class': 'form-control'}))
        trees = CategoryUtil.getCategoryTree(module_id, 0, '|', '')
        # trees = [('0', '顶级分类')] + trees
        self.fields['cat_id'].choices = trees

        self.fields['cover'] = forms.ImageField(label=u'封面', required=False)

        '''文章内容'''
        # self.fields['content'] = forms.CharField(label=u'内容', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 20}))
        self.fields['content'] = forms.CharField(label=u'内容', widget=UEditorWidget(
            attrs={'width': '100%', 'height': 400, 'imagePath': 'upload/images/', 'filePath': 'upload/files/',
                   'toolbars': [[
                       'fullscreen', 'source', '|', 'undo', 'redo', '|', 'bold', 'italic', 'underline', 'fontborder',
                       'strikethrough',
                       'superscript', 'subscript', 'removeformat', 'formatmatch', 'autotypeset', 'blockquote',
                       'pasteplain', '|',
                       'forecolor', 'backcolor', 'insertorderedlist', 'insertunorderedlist', 'selectall', '|',
                       'simpleupload', 'insertimage', 'emotion', 'insertvideo', 'music', 'attachment', 'map', 'gmap',
                       'insertcode', 'webapp', 'pagebreak', 'template', '|', 'selectall', 'cleardoc'
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
