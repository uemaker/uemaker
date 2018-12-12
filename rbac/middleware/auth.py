import re
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.shortcuts import render, redirect, HttpResponse


class AuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        request_url = request.path_info

        safe_urls = settings.RBAC.get('safe_urls', [])
        for each in safe_urls:
            if re.match(each, request_url):
                return None

        reg_manage = '^/manage/'
        reg_rbac = '^/rbac/'
        reg_book = '^/book/'
        return None
        # if not re.match(reg_manage, request_url) and not re.match(reg_rbac, request_url):
        #     return None

        permission_dict = request.session.get('rbac_authorized_permission', {})
        if not permission_dict:
            return redirect('/rbac/login/')

        # has_permission = False
        has_permission = True
        for code, permission in permission_dict.items():
            regax = '^{0}$'.format(code)
            if re.match(regax, request_url):
                has_permission = True
                break

        if not has_permission:
            return HttpResponse('无权访问')

    def process_response(self, request, response):
        return response
