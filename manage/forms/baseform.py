import decimal
from DjangoUeditor.widgets import UEditorWidget
from django import forms

from manage.utils import FieldUtil


class BaseModelForm(forms.ModelForm):

    def createField(self, field=None, extra_val=None, is_update=False):
        blank = field['blank']
        default = extra_val if is_update else field['default']
        if field['type'] == FieldUtil.FIELD_TEXT:
            self.fields[field['name']] = forms.CharField(
                label=field['title'],
                max_length=int(field['length']),
                required=blank,
                initial=default,
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
                initial=default,
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
                initial=default,
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
                initial=int(default),
                help_text=field['help_text'],
                widget=forms.NumberInput(
                    attrs={'class': 'form-control'},
                )

            )
        elif field['type'] == FieldUtil.FIELD_SELECT:
            self.fields[field['name']] = forms.ChoiceField(
                label=field['title'],
                required=blank,
                initial=default,
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
                initial=default,
                help_text=field['help_text'],
                widget=forms.CheckboxInput(
                )

            )
        elif field['type'] == FieldUtil.FIELD_RADIO:
            self.fields[field['name']] = forms.BooleanField(
                label=field['title'],
                required=blank,
                initial=int(default),
                help_text=field['help_text'],
                widget=forms.RadioSelect(
                    attrs={},
                )

            )
        elif field['type'] == FieldUtil.FIELD_IMAGE:
            default = extra_val if is_update else None
            self.fields[field['name']] = forms.ImageField(
                label=field['title'],
                required=blank,
                initial=default,
                help_text=field['help_text'],
            )
        elif field['type'] == FieldUtil.FIELD_FILE:
            default = extra_val if is_update else None
            self.fields[field['name']] = forms.FileField(
                label=field['title'],
                required=blank,
                initial=default,
                help_text=field['help_text'],
            )
        elif field['type'] == FieldUtil.FIELD_DATETIME:
            default = extra_val if is_update else None
            self.fields[field['name']] = forms.DateTimeField(
                label=field['title'],
                required=blank,
                initial=default,
                help_text=field['help_text'],
            )
        elif field['type'] == FieldUtil.FIELD_DATE:
            default = extra_val if is_update else None
            self.fields[field['name']] = forms.DateField(
                label=field['title'],
                required=blank,
                initial=default,
                help_text=field['help_text'],
            )
        elif field['type'] == FieldUtil.FIELD_TIME:
            default = extra_val if is_update else None
            self.fields[field['name']] = forms.TimeField(
                label=field['title'],
                required=blank,
                initial=default,
                help_text=field['help_text'],
            )
        elif field['type'] == FieldUtil.FIELD_EMAIL:
            self.fields[field['name']] = forms.EmailField(
                label=field['title'],
                required=blank,
                help_text=field['help_text'],
                initial=default,
                widget=forms.ClearableFileInput(
                    attrs={'class': 'form-control'},
                )
            )
        elif field['type'] == FieldUtil.FIELD_DECIMAL:
            default = field['default'] if decimal.Decimal(field['default']) else None
            default = extra_val if is_update else default
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
            default = extra_val if is_update else default
            self.fields[field['name']] = forms.FloatField(
                label=field['title'],
                required=blank,
                help_text=default,
                initial=float(field['default']),
                widget=forms.NumberInput(
                    attrs={'class': 'form-control'},
                )
            )
