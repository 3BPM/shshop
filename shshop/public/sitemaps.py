#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :sitemaps.py
@说明    :站点地图
@时间    :2023/03/23 21:03:40

'''


from django.contrib.sitemaps import Sitemap
from django.contrib.flatpages.sitemaps import FlatPageSitemap

from shshop import models


class ShShopSPUSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return models.ShShopSPU.objects.filter(is_del=False)

    def lastmod(self, obj):
        return obj.pub_date


class ShShopCategorySitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return models.ShShopCategory.objects.filter(is_del=False)

    def lastmod(self, obj):
        return obj.pub_date


sitemaps = {
    'spu': ShShopSPUSitemap,
    'cate': ShShopCategorySitemap,
    'flatpage': FlatPageSitemap
}