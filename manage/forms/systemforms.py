import json

from django import forms
from django.core.validators import RegexValidator
from django.db.models import Q

from manage.models import Module, ModuleField, Category
from manage.utils import ModuleUtil, FieldUtil, CategoryUtil


class ModuleForm(forms.ModelForm):

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

    def clean_name(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.name
        else:
            return self.cleaned_data['name']

    def __init__(self, *args, **kwargs):
        super(ModuleForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        is_update = True if instance and instance.pk else False
        self.fields['name'] = forms.CharField(
            label=u'模块标识',
            widget=forms.TextInput(attrs={'class': 'form-control'}, ),
            disabled=is_update,
            min_length=2,
            max_length=20,
            help_text='模块标识，由英文字母组成，长度为2-20个字符。',
            validators=[RegexValidator(r'^[a-zA-z]+$', '模块标识格式错误'), ],
        )
        config = {}
        if is_update:
            config = json.loads(instance.config) if instance.config else {}

        self.fields['is_front'] = forms.BooleanField(
            label='启用分享功能',
            initial=config.get('is_front', True),
            required=False,
            widget=forms.CheckboxInput()
        )

        self.fields['password'] = forms.BooleanField(
            label='启用查看加密',
            initial=config.get('password', False),
            required=False,
            widget=forms.CheckboxInput()
        )

    def save(self, commit=True):
        media = super(ModuleForm, self).save(commit=False)
        config = {
            'is_front': self.cleaned_data['is_front'],
            'password': self.cleaned_data['password']
        }
        media.config = json.dumps(config)
        if commit:
            media.save()

class ModuleFieldForm(forms.ModelForm):

    class Meta:
        model = ModuleField
        fields = ['module_id', 'type', 'name', 'title', 'length', 'blank', 'default', 'help_text', 'value', 'sort']
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
            'sort': forms.NumberInput(attrs={'class': 'form-control'},),
        }
        help_texts = {
            'title': '字段说明文字，表单中输入项的label标签文字。',
            'help_text': '表单中输入框下面的提示文字。',
            'value': 'select选项，key=value的形式（例如: 1=中国），每行一个选项，最长为200个字符。',
        }

    def clean_name(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.name
        else:
            return self.cleaned_data['name']

    def clean(self):
        name = self.cleaned_data.get('name')
        module_id = self.cleaned_data.get('module_id')
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            count = ModuleField.objects.filter(module_id=module_id, name=name).filter(~Q(id=self.instance.pk)).count()
        else:
            count = ModuleField.objects.filter(module_id=module_id, name=name).count()
        if count > 0:
            self.add_error("name", name+"已存在")
        return self.cleaned_data

    def __init__(self, *args, **kwargs):
        module_id = kwargs.pop('module_id', None)
        super(ModuleFieldForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        disabled = True if instance and instance.pk else False

        self.fields['name'] = forms.CharField(
            label=u'字段名称',
            widget=forms.TextInput(attrs={'class': 'form-control'},),
            disabled=disabled,
            min_length=2,
            max_length=20,
            help_text='数据库字段名，字段唯一标识，由英文字母和下划线组成，长度为2-20个字符。',
            validators=[RegexValidator(r'^[a-zA-z_]+$', '字段名称格式错误'), ],
        )

        self.fields['type'] = forms.ChoiceField(label=u'字段类型', disabled=disabled, widget=forms.Select(attrs={'class': 'form-control'}))
        self.fields['type'].choices = FieldUtil.getFieldOptions()
        self.fields['module_id'].initial = module_id

    def save(self, commit=True):
        media = super(ModuleFieldForm, self).save(commit=False)
        if commit:
            instance = getattr(self, 'instance', None)
            if not instance or not instance.pk:
                media.name = 'f_'+media.name
            media.save()

class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ['pid', 'module_id', 'name', 'title', 'sort']
        widgets = {
            'module_id': forms.HiddenInput(),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'sort': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        module_name = kwargs.pop('module_name', None)
        pid = kwargs.pop('pid', None)
        super(CategoryForm, self).__init__(*args, **kwargs)
        module_id = ModuleUtil.getModuleId(module_name)
        self.fields['pid'] = forms.ChoiceField(label=u'上级分类', initial=pid, widget=forms.Select(attrs={'class': 'form-control'}))
        trees = CategoryUtil.getCategoryTree(module_id, 0, '|')
        trees = [('0', '顶级分类')] + trees
        self.fields['pid'].choices = trees
        self.fields['module_id'].initial = module_id
