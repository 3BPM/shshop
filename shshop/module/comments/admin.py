from django.contrib import admin

from shshop.public.admin import BaseModelAdmin
from shshop.public.sites import sh_site
from shshop.models import ShOrderInfoComments


@admin.register(ShOrderInfoComments, site=sh_site)
class ShOrderInfoCommentsAdmin(BaseModelAdmin):
    list_display = ('id', 'owner', 'comment_choices', 'content')

    def has_change_permission(self, request, obj=None) -> bool:
        return False

    def has_add_permission(self, request) -> bool:
        return False