#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :abstract.py
@说明    :模型基类
@时间    :2023/02/19 17:28:56
@作者    :幸福关中&轻编程
@版本    :1.0
@微信    :baywanyun
'''


from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _

from shshop.public.manager import BaseManager
# Create your models here.


class AbstractModel(models.Model):
    """ 基类 """
    add_date = models.DateTimeField(auto_now_add=True)
    pub_date = models.DateTimeField(auto_now=True)
    is_del = models.BooleanField(default=False, editable=False)

    objects = BaseManager()

    class Meta:
        ordering = ['-add_date']
        abstract = True


class CategoryAbstractModel(AbstractModel):
    """ 分类基类 """

    name = models.CharField("分类名称", max_length=50)
    icon = models.CharField("分类icon", max_length=50, blank=True, default="")
    img_map = models.ImageField(
        "推荐图",
        upload_to="category/imgMap/%Y",
        max_length=200,
        blank=True,
        null=True,
        help_text="图片尺寸为600 X 480"
    )
    desc = models.CharField("分类描述", max_length=150, blank=True, default="")

    class Meta:
        ordering = ['-add_date']
        abstract = True


class CarouselAbstractModel(AbstractModel):
    """ 轮播图基类 """

    img = models.ImageField("轮播图", upload_to="carousel/%Y/%m", max_length=200,)
    target_url = models.CharField("跳转链接", blank=True, default="", max_length=200)
    desc = models.CharField("描述", max_length=150, blank=True, default="")

    class Meta:
        ordering = ['-add_date']
        abstract = True


class ContentTypeAbstract(AbstractModel):
    """ 模型的通用关系 """
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]