from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.base import View
from django.shortcuts import render, redirect, HttpResponse

from rbac import forms
from rbac.services.permission import load_permissions


class LoginView(View):

    def get(self, request, *args, **kwargs):
        form = forms.LoginForm()
        return render(request, 'rbac/login.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            request.session['is_login'] = 'true'
            request.session['user'] = {
                'username': data['username'],
            }
            load_permissions(request, form.user)
            return redirect('/manage/')

        return render(request, 'rbac/login.html', {'form': form})
