#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :models.py
@说明    :站点统计模块
@时间    :2023/03/22 09:15:19
@作者    :幸福关中&轻编程
@版本    :1.0
@微信    :baywanyun
'''

from django.db import models
from shshop.public.abstract import AbstractModel, ContentTypeAbstract


class ShIPAddress(AbstractModel):
    """ 统计站点来访IP """
    ip = models.GenericIPAddressField(null=True, blank=True)
    browser = models.TextField(max_length=500, blank=True, default="")
    address = models.CharField(max_length=150, blank=True, default="")

    class Meta:
        verbose_name = 'ShStatsIPAddress'
        verbose_name_plural = 'ShStatsIPAddress'

    def __str__(self):
        return self.address


class ShStats(ContentTypeAbstract):
    """ pv 和 uv统计 """
    pv = models.BigIntegerField(default=0)
    uv = models.BigIntegerField(default=0)

    class Meta:
        verbose_name = 'ShStats'
        verbose_name_plural = 'ShStatss'

    def __str__(self):
        return f"pv:{self.pv} | uv: {self.uv}"


