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

        permission_list = request.session.get('rbac_permission_list', [])
        if not permission_list:
            redirect('/rbac/login/')

        has_permission = False
        for permission in permission_list:
            regax = '^{0}$'.format(permission.get('code'))
            if re.match(regax, request_url):
                has_permission = True
                break

        if not has_permission:
            return HttpResponse('无权访问')

    def process_response(self, request, response):
        return response
