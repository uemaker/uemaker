from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import hashers
from django.core.validators import RegexValidator

from rbac import models
from rbac.models import User


class LoginForm(forms.Form):

    username = forms.CharField(
        label=u'用户名',
        max_length=20,
        required=True,
        strip=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'autofocus': 'autofocus',
                'placeholder': '请输入用户名'
            }
        ),
        error_messages={'required': '用户名不能为空', }
    )
    password = forms.CharField(
        label=u'用户名',
        max_length=20,
        required=True,
        strip=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'autofocus': 'autofocus',
                'placeholder': '请输入密码',
            }
        ),
        error_messages={'required': '密码不能为空', }
    )

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = models.User.objects.get_by_name(username)
        if username and password:
            if not user:
                raise ValidationError('用户名不存在！')
            elif not user.check_password(password):
                raise ValidationError('密码不正确！')
            self.user = user


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        is_update = True if instance and instance.pk else False

        self.fields['username'] = forms.CharField(
            label=u'用户名',
            widget=forms.TextInput(attrs={'class': 'form-control'}, ),
            disabled=is_update,
            min_length=2,
            max_length=20,
            help_text='用户名由中英文、数字和下划线组成，且首字母不能为数字，长度为2-20个字符。',
            validators=[RegexValidator(r'^[a-zA-Z\u4e00-\u9fa5]+[\\w\u4e00-\u9fa5]*$', '用户名格式错误'), ],
        )

        self.fields['email'] = forms.CharField(
            label=u'邮箱',
            widget=forms.EmailInput(attrs={'class': 'form-control'}, ),
            required=False,
        )

        if not is_update:
            self.fields['password'] = forms.CharField(
                label=u'密码',
                widget=forms.PasswordInput(attrs={'class': 'form-control'}, ),
                min_length=6,
                max_length=12,
                help_text='密码由大小写字母、数字，下划线及特殊字符组成，长度为6-12个字符。',
                validators=[RegexValidator(r'[\\w\$\(\)\*\+\.\[\?\\\^\{\|!@#%&-=]+$', '密码格式错误'), ],
            )

        if is_update:
            self.Meta.fields.append('real_name')
            self.Meta.fields.append('is_super')
            self.Meta.fields.append('is_active')
            self.fields['real_name'] = forms.CharField(
                label=u'真实姓名',
                widget=forms.TextInput(attrs={'class': 'form-control'}, ),
                max_length=20,
                required=False,
            )

            self.fields['is_super'] = forms.BooleanField(
                label='是否为首级管理员',
                required=False,
                widget=forms.CheckboxInput()
            )

            self.fields['is_active'] = forms.BooleanField(
                label='是否可用',
                required=False,
                widget=forms.CheckboxInput()
            )


