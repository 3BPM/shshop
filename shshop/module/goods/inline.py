from django.contrib import admin

from shshop.models import (
    ShShopCategory, ShShopSKU,
    ShSPUCarousel, ShShopSpecOption
)


class ShShopCategoryInline(admin.TabularInline):
    '''Tabular Inline View for ShShopCategory'''

    model = ShShopCategory
    min_num = 1
    max_num = 20
    extra = 1
    exclude = ('img_map', )
    # raw_id_fields = (,)

class ShShopSKUInline(admin.TabularInline):
    '''Stacked Inline View for ShShopSKU'''

    model = ShShopSKU
    # min_num = 1
    max_num = 20
    extra = 1
    can_delete = False
    # raw_id_fields = (,)


class ShSPUCarouselInline(admin.StackedInline):
    '''Tabular Inline View for '''

    model = ShSPUCarousel
    min_num = 1
    max_num = 20
    extra = 1
    exclude = ('target_url', 'desc')
    # raw_id_fields = (,)


class ShShopSpecOptionInline(admin.StackedInline):
    '''Stacked Inline View for '''

    model = ShShopSpecOption
    min_num = 1
    max_num = 20
    extra = 1