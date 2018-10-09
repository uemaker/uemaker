import json

from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView
from django.views.generic.base import View
from django.views.generic.edit import CreateView, UpdateView

from rbac import forms
from rbac.forms import UserForm
from rbac.models import User
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
            admin_url = settings.RBAC.get('admin_url', '/manage/')
            return redirect(admin_url)

        return render(request, 'rbac/login.html', {'form': form})


class UserListView(ListView):
    template_name = 'rbac/user_list.html'
    context_object_name = "data"
    paginate_by = 100

    def post(self, request, *args, **kwargs):
        user_id = request.POST.get('id')
        data = {}
        if user_id:
            User.objects.get(id=user_id).delete()
            data['success'] = 1
        else:
            data['success'] = 0

        return HttpResponse(json.dumps(data), content_type="application/json")

    def get_queryset(self, *args, **kwargs):
        data = {}
        data = User.objects.filter()

        return data

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        context['form_url'] = reverse('users')
        return context


class UserCreateView(CreateView):
    form_class = UserForm
    template_name = 'rbac/form/create_form.html'
    success_url = 'users'

    def form_valid(self, form):
        if form.is_valid:
            form.Meta.model.objects.create_user(form.cleaned_data['username'], form.cleaned_data['email'], form.cleaned_data['password'])
            return HttpResponseRedirect(reverse(self.success_url))

    def get_context_data(self, **kwargs):
        context = super(UserCreateView, self).get_context_data(**kwargs)
        context['form_url'] = reverse('add_user')
        context['form_title'] = '添加管理员'
        return context


class UserUpdateView(UpdateView):
    model = User
    template_name = 'rbac/form/create_form.html'
    form_class = UserForm
    success_url = 'users'

    def get_context_data(self, **kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        context['form_url'] = reverse('edit_user', kwargs={'pk': self.kwargs.get(self.pk_url_kwarg)})
        context['form_title'] = '编辑管理员'
        return context

    def form_valid(self, form):
        if form.is_valid:
            form.Meta.model.objects.update_user(form.instance.pk, username=form.cleaned_data.get('username'), email=form.cleaned_data.get('email'), real_name=form.cleaned_data.get('real_name'), is_super=form.cleaned_data.get('is_super', False), is_active=form.cleaned_data.get('is_active', False))
            return HttpResponseRedirect(reverse(self.success_url))
