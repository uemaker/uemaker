from django import forms
from manage.models import Module

class ModuleAddForm(forms.ModelForm):

    class Meta:
        model = Module
        fields = ['name', 'title', 'sort']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'sort': forms.TextInput(attrs={'class': 'form-control'}),
        }
