from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import hashers

from rbac import models

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
