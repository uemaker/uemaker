from django import forms
from manage.models import Module
from manage.models import Category
from manage.models import ModuleField
from manage.utils import TreeUtil
from manage.utils import FieldUtil
import json

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


