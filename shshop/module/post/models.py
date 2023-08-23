# #!/usr/bin/env python
# # -*- encoding: utf-8 -*-
# '''
# @文件    :post.py
# @说明    :发送商品模型


from django.db import models
from django.contrib.auth import get_user_model

from shshop.public.abstract import AbstractModel
from shshop.models import ShShopSKU

User = get_user_model()


class GoodPost(AbstractModel):

#     """ 购物车数据模型 """
#     owner = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="用户")
#     sku = models.ForeignKey(ShShopSKU, on_delete=models.PROTECT, verbose_name="商品sku")
#     num = models.PositiveIntegerField(default=0, verbose_name="数量")

    class Meta:
        verbose_name = '推送商品'
#         verbose_name_plural = verbose_name
#         constraints = [
#             models.UniqueConstraint(fields=['owner', 'sku'], name='unique_owner_sku')
#         ]

#     def __str__(self):
#         return f'{self.owner}{self.sku}'

#     @classmethod
#     def get_post_count(cls, user):
#         # 当前用户的购物车商品数量
#         return sum(list(cls.objects.filter(owner=user).values_list('num', flat=True)))