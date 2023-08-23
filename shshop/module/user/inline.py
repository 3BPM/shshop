from django.contrib import admin

from shshop.models import (ShPermission, UserInfo)


class UserInfoInline(admin.StackedInline):
    '''Tabular Inline View for UserInfo'''
    model = UserInfo


class ShPermissionInline(admin.TabularInline):
    '''Tabular Inline View for ShPermission'''

    model = ShPermission
    min_num = 1
    max_num = 20
    extra = 1
    # raw_id_fields = (,)
