from django import forms
from manage.models import Module
from manage.models import Category
from manage.models import ModuleField
from manage.utils import TreeUtil
from manage.utils import FieldUtil
import json

class ModuleAddForm(forms.ModelForm):

    class Meta:
        model = Module
        fields = ['name', 'title', 'desc']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'},),
            'desc': forms.Textarea(attrs={'class': 'form-control'}),
        }
        help_texts = {
            'desc': '限200个字符'
        }

class ModuleUpdateForm(forms.ModelForm):

    status = forms.BooleanField(required=False, label='状态')

    class Meta:
        model = Module
        fields = ['name', 'title', 'desc']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'},),
            'desc': forms.Textarea(attrs={'class': 'form-control'}),
        }
        help_texts = {
            'desc': '限200个字符'
        }

    def save(self, commit=True):
        media = super(ModuleUpdateForm, self).save(commit=False)
        status = self.cleaned_data['status']
        config = {'status': status}
        media.config = json.dumps(config)
        if commit:
            media.save()

class ModuleFieldForm(forms.ModelForm):

    class Meta:
        model = ModuleField
        fields = ['module_id', 'type', 'name', 'title', 'length', 'blank', 'default', 'help_text', 'value']
        widgets = {
            'module_id': forms.HiddenInput(),
            'name': forms.TextInput(attrs={'class': 'form-control'},),
            'title': forms.TextInput(attrs={'class': 'form-control'},),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'length': forms.NumberInput(attrs={'class': 'form-control'}, ),
            'blank': forms.CheckboxInput(),
            'default': forms.TextInput(attrs={'class': 'form-control'},),
            'help_text': forms.TextInput(attrs={'class': 'form-control'},),
            'value': forms.Textarea(attrs={'class': 'form-control'},),
        }
        help_texts = {
            'name': '只允许输入英文字母和下划线，最长为20个字符',
            'value': 'select选项，每行一个选项，最长为200个字符',
        }

    def __init__(self, *args, **kwargs):
        module_id = kwargs.pop('module_id', None)
        super(ModuleFieldForm, self).__init__(*args, **kwargs)
        self.fields['type'] = forms.ChoiceField(label=u'字段类型', widget=forms.Select(attrs={'class': 'form-control'}))
        self.fields['type'].choices = FieldUtil.getFieldOptions()
        self.fields['module_id'].initial = module_id

class CategoryAddForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ['pid', 'module_id', 'name', 'title', 'sort']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'sort': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(CategoryAddForm, self).__init__(*args, **kwargs)
        self.fields['module_id'] = forms.ChoiceField(label=u'所属模块', widget=forms.Select(attrs={'class': 'form-control'}))
        self.fields['module_id'].choices = Module.objects.values_list('id', 'title')
        self.fields['pid'] = forms.ChoiceField(label=u'上级分类', widget=forms.Select(attrs={'class': 'form-control'}))
        trees = TreeUtil.getChildNodeTree(0, '|')
        trees = [('0', '顶级分类')] + trees
        self.fields['pid'].choices = trees
