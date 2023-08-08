#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :product.py
@说明    :商品相关模型
@时间    :2023/02/19 17:38:25
@作者    :幸福关中&轻编程
@版本    :1.0
@微信    :baywanyun
'''

from django.db import models
from django.urls import reverse

# Create your models here.
from shshop.config.settings import sh_settings
from shshop.public.abstract import (
    AbstractModel, CategoryAbstractModel,
    CarouselAbstractModel
)
from shshop.public.tinymce import TinymceField
from django.contrib.auth import get_user_model
User = get_user_model()


class ShShopCategory(CategoryAbstractModel):
    """ 商品分类 """
    parent = models.ForeignKey(
        'self',
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )
    is_home = models.BooleanField(
        default=False,
        verbose_name="是否推荐",
        help_text="如果为True则推荐到首页楼层及出现在导航菜单"
    )

    class Meta:
        ordering = ['-add_date']
        verbose_name = '商品分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    @classmethod
    def get_cates(cls):
        cates = cls.objects.filter(is_home=True, parent__isnull=True)
        for cate in cates:
            cate.sub_cates = cate.shshopcategory_set.filter(is_home=True)
        return cates

    def get_absolute_url(self):
        return reverse('shshop:cate_detail', kwargs={'pk': self.pk})


class ShShopSPU(AbstractModel):
    """SPU"""

    title = models.CharField("商品名称", max_length=150)
    keywords = models.CharField(
        "商品关键字", max_length=150, blank=True, default="")
    desc = models.CharField("商品描述", max_length=200, blank=True, default="")
    category = models.ManyToManyField(ShShopCategory, verbose_name="商品分类")
    unit = models.CharField("单位", max_length=50)
    cover_pic = models.ImageField(
        "封面图", upload_to="product/cover/spu/%Y/%m", max_length=200)
    freight = models.DecimalField(
        "运费", max_digits=5, decimal_places=2, blank=True, default=0.00)
    # content = models.TextField("商品详情")#TODO
    content = TinymceField("商品详情",blank=True)

    owner = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="用户")
    class Meta:
        ordering = ['-add_date']
        verbose_name = '商品管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

    @classmethod
    def get_hots(cls):
        # 热销商品
        return cls.objects.order_by('-shshopsku__sales')[:sh_settings.HOT_SPUS_LEN]

    def get_absolute_url(self):
        return reverse('shshop:spu_detail', kwargs={'pk': self.pk})


class ShShopSpec(AbstractModel):
    """ 规格 """
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="规格"
    )

    class Meta:
        verbose_name = '发布区域'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class ShShopSpecOption(AbstractModel):
    """ 规格值 """

    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="规格值"
    )
    spec = models.ForeignKey(
        ShShopSpec,
        on_delete=models.PROTECT,
        verbose_name="规格"
    )

    class Meta:
        verbose_name = '规格值'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.spec.name} - {self.name}"


class ShShopSKU(AbstractModel):
    """ SKU """
    spu = models.ForeignKey(
        ShShopSPU, on_delete=models.PROTECT, verbose_name="商品")
    options = models.ManyToManyField(
        ShShopSpecOption, blank=True, verbose_name="发布区域")
    cover_pic = models.ImageField(
        "封面图",
        upload_to="cover/sku/%Y/%m",
        max_length=200
    )
    price = models.DecimalField("售价", max_digits=8, decimal_places=2)
    cost_price = models.DecimalField("成本价", max_digits=8, decimal_places=2)
    org_price = models.DecimalField("原价", max_digits=8, decimal_places=2)
    stock = models.IntegerField("库存", default=0)
    sales = models.PositiveIntegerField("销量", default=0, editable=False)
    numname = models.CharField("商品成色", max_length=50, default="", blank=True)
    weight = models.FloatField("重量(KG)", default=0, blank=True)
    vol = models.FloatField("体积(m³)", default=0, blank=True)

    class Meta:
        verbose_name = 'ShShopSKU'
        verbose_name_plural = 'ShShopSKUs'

    def __str__(self):
        return self.spu.title


class ShSPUCarousel(CarouselAbstractModel):
    """ spu轮播图 """
    product = models.ForeignKey(ShShopSPU, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'ShSPUCarousel'
        verbose_name_plural = 'ShSPUCarousels'

    def __str__(self):
        return f"{self.img.name}"