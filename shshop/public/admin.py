from django.contrib import admin
from django.contrib.sites.admin import SiteAdmin
from django.contrib.sites.models import Site
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from shshop.public.forms import ShFlatpageForm
from shshop.public.sites import sh_site
from shshop.models import ShBanner


# Re-register FlatPageAdmin
admin.site.unregister(FlatPage)
admin.site.unregister(Site)


class BaseModelAdmin(admin.ModelAdmin):
    """继承了django的ModelAdmin
    重写并新增了一些全局方法
    """
    change_list_template = "shadmin/change_list.html"
    change_form_template = "shadmin/change_form.html"

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if self.model._meta.model_name not in ['user', 'group', 'permission', 'logentry']:
            queryset = queryset.filter(is_del=False)
        return queryset

    def change_view(self, request, object_id, form_url="", extra_context=None):
        return super().change_view(request, object_id, form_url, extra_context)

    @admin.display(description="操作")
    def operate(self, obj):
        hs = '<a href="{}">编辑</a> | <a href="{}">删除</a>'
        h1 = reverse(f'shadmin:{obj._meta.app_label}_{obj._meta.model_name}_change', args=(obj.pk, ))
        h2 = reverse(f'shadmin:{obj._meta.app_label}_{obj._meta.model_name}_delete', args=(obj.pk, ))
        return format_html(hs, h1, h2)


@admin.register(ShBanner, site=sh_site)
class ShShopBannerAdmin(BaseModelAdmin):
    list_display = ('id', 'imgformat', 'target_url', 'operate')

    @admin.display(description="轮播图")
    def imgformat(self, obj):
        return format_html(f'<img src="{obj.img.url}" width="auto" height="100px" />')

    class Media:
        css = {'all': ['shadmin/css/ordersku.css']}


# Define a new FlatPageAdmin
@admin.register(FlatPage, site=sh_site)
class FlatPageAdmin(FlatPageAdmin):

    change_list_template = "shadmin/change_list.html"
    change_form_template = "shadmin/change_form.html"
    form = ShFlatpageForm

    fieldsets = (
        (None, {'fields': ('url', 'title', 'content', 'sites')}),
        (_('Advanced options'), {
            'classes': ('collapse',),
            'fields': (
                'enable_comments',
                'registration_required',
                'template_name',
            ),
        }),
    )


@admin.register(Site, site=sh_site)
class SiteAdmin(SiteAdmin):
    pass