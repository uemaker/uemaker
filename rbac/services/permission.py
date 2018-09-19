import json

from django.core import serializers

from rbac.models import Group, Menu


def load_permissions(request, user):

    group_permission_list = user.groups.values('permissions__id', 'permissions__name', 'permissions__code', 'permissions__is_menu').distinct()
    user_permission_list = user.permissions.values('id', 'name', 'code', 'is_menu').distinct()

    if not group_permission_list:
        group_permission_list = []
    if not user_permission_list:
        user_permission_list = []

    permission_list = group_permission_list + user_permission_list
    if not permission_list:
        permission_list = list(set([tuple(t) for t in permission_list]))

    menu_permission_list = Menu.objects.filter().values_list('id', 'name', 'permissions__id', 'permissions__name', 'permissions__code', 'permissions__is_menu').distinct()

    request.session['authorized_menu'] = serializers.serialize("json", menu_permission_list)


