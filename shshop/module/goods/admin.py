from django.contrib import admin
from django.utils.html import format_html, format_html_join
from django.utils.safestring import mark_safe
# Register your models here.
from shshop.public.admin import BaseModelAdmin
from shshop.models import (
    ShShopCategory, ShShopSPU,
    ShShopSKU, ShShopSpec
)
from shshop.public.sites import sh_site

from shshop.module.goods.inline import (
    ShShopCategoryInline, ShShopSKUInline,
    ShSPUCarouselInline, ShShopSpecOptionInline
)
from shshop.module.goods.forms import ShShopSPUForm


@admin.register(ShShopCategory, site=sh_site)
class ShShopCategoryAdmin(BaseModelAdmin):
    list_display = ('id', 'name', 'parent', 'operate')
    exclude = ('parent',)
    inlines = (ShShopCategoryInline, )
    # search_fields = ('parent__name',)
    # autocomplete_fields = ('parent', )

    def get_queryset(self, request):
        return super().get_queryset(request).filter(parent__isnull=True)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'parent':
            kwargs['queryset'] = ShShopCategory.objects.filter(parent__isnull=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(ShShopSPU, site=sh_site)
class ShShopSPUAdmin(BaseModelAdmin):
    list_display = (
        'id',
        'owner',
        'dis_cover_pic',
        'title',
        'dis_price',
        'dis_spec',
        'dis_sales',
        'dis_stock',
        'operate',

    )
    list_display_links = ('title', )
    filter_horizontal = ('category',)
    # form = ShShopSPUForm
    inlines = (ShShopSKUInline, ShSPUCarouselInline)

    class Media:
        css = {'all': ['shadmin/css/ordersku.css']}

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            kwargs['queryset'] = ShShopCategory.objects.filter(parent__isnull=False)
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def get_skus(self, obj):
        return obj.shshopsku_set.order_by('price')

    @admin.display(description="封面图")
    def dis_cover_pic(self, obj):
        return format_html(mark_safe("<img width='64px' height='64px' src='{}' />"), obj.cover_pic.url)

    @admin.display(description="价格")
    def dis_price(self, obj):
        return self.get_skus(obj).first().price

    @admin.display(description="包含规格")
    def dis_spec(self, obj):
        return format_html_join(
            '\n', '{}<br>',
            (
               (f"{k['spec__name']}:{k['name']}" for k in u.options.values('spec__name','name',)) for u in self.get_skus(obj) if u.options.exists()
            )
        )

    @admin.display(description="销量")
    def dis_sales(self, obj):
        from django.db.models import Sum
        return self.get_skus(obj).aggregate(Sum('sales'))['sales__sum']

    @admin.display(description="库存")
    def dis_stock(self, obj):
        from django.db.models import Sum
        return self.get_skus(obj).aggregate(Sum('stock'))['stock__sum']


@admin.register(ShShopSKU, site=sh_site)
class ShShopSKUAdmin(BaseModelAdmin):
    list_display = ('id', 'spu')
    # inlines = (ShShopSKUInline, )
    filter_horizontal = ('options',)
    # autocomplete_fields = ('options', )


@admin.register(ShShopSpec, site=sh_site)
class ShShopSpecAdmin(BaseModelAdmin):
    list_display = ('id', 'name', 'operate')
    search_fields = ('name',)
    inlines = (ShShopSpecOptionInline, )