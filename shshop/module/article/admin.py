from django.contrib import admin

from shshop.public.sites import sh_site
from shshop.public.admin import BaseModelAdmin
from shshop.models import ShArticle, ShArticleCategory, ShArticleTags


@admin.register(ShArticleCategory, site=sh_site)
class ShArticleCategoryAdmin(BaseModelAdmin):
    '''Admin View for ShArticleCategory'''

    list_display = ('name', 'icon', 'desc', 'add_date')
    search_fields = ('name', 'desc')


@admin.register(ShArticle, site=sh_site)
class ShArticleAdmin(BaseModelAdmin):
    '''Admin View for ShArticleCategory'''

    list_display = ('title', 'category', 'add_date')
    search_fields = ('title', 'desc')

    def save_model(self, request, obj, form, change) -> None:
        obj.owner = request.user
        return super().save_model(request, obj, form, change)


sh_site.register(ShArticleTags)