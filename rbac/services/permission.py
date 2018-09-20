from django.core import serializers
from django.db.models import F

from rbac.models import Menu


def load_permissions(request, user):

    group_permission_list = user.groups.annotate(
        pm_id=F("permissions__id"),
        pm_name=F("permissions__name"),
        pm_code=F("permissions__code"),
        is_menu=F("permissions__is_menu"),
    ).values('pm_id', 'pm_name', 'pm_code', 'is_menu').distinct()
    user_permission_list = user.permissions.annotate(
        pm_id=F("id"),
        pm_name=F("name"),
        pm_code=F("code"),
    ).values('pm_id', 'pm_name', 'pm_code', 'is_menu').distinct()
    group_permission_list = list(group_permission_list) if group_permission_list else []
    user_permission_list = list(user_permission_list) if user_permission_list else []
    permission_list = group_permission_list + user_permission_list

    permission_dict = {}
    if permission_list:
        key_arr = []
        for permission in permission_list:
            if not permission.get('pm_id') in key_arr:
                permission_dict[permission.get('pm_code')] = permission
                key_arr.append(permission.get('pm_id'))

    request.session['authorized_permission'] = permission_dict

    menu_permission_list = Menu.objects.filter().annotate(
        pm_id=F("permissions__id"),
        pm_name=F("permissions__name"),
        pm_code=F("permissions__code"),
        is_menu=F("permissions__is_menu"),
    ).values('id', 'name', 'pm_id', 'pm_name', 'pm_code', 'is_menu').distinct()
    menu_permission_list = list(menu_permission_list) if menu_permission_list else []
    menu_permission_dict = {}
    print(menu_permission_list)
    if menu_permission_list:
        key_arr = []
        for menu_permission in menu_permission_list:
            if not menu_permission.get('pm_id') in key_arr:
                if menu_permission.get('name') in menu_permission_dict:
                    menu_permission_dict[menu_permission.get('name')].append(menu_permission)
                else:
                    menu_permission_dict[menu_permission.get('name')] = [menu_permission]
                key_arr.append(menu_permission.get('pm_id'))

    request.session['authorized_menu'] = menu_permission_dict

    print(request.session.get('authorized_menu'))



