from django import forms
from manage.models import Module
from manage.models import Category

class ModuleAddForm(forms.ModelForm):

    class Meta:
        model = Module
        fields = ['name', 'title', 'sort']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'sort': forms.TextInput(attrs={'class': 'form-control'}),
        }

class CategoryAddForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ['pid', 'module','name', 'title', 'sort']
        widgets = {
            'pid': forms.Select(choices=[('0', '顶级分类')], attrs={'class': 'form-control'}),
            'module': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'sort': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(CategoryAddForm, self).__init__(*args, **kwargs)
        self.fields['module'].choices = Module.objects.values_list('id', 'title')
