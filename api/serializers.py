from rest_framework import serializers
from shshop.public.models import (ShMenu, ShPermission, ShBanner,
                                     ShUpload)

from shshop.module.user.models import (UserInfo, ShUserBalanceLog,
                                          ShShopAddress)

from shshop.module.goods.models import (ShShopCategory, ShShopSPU,
                                           ShShopSpec, ShShopSpecOption,
                                           ShShopSKU, ShSPUCarousel)

from shshop.module.cart.models import ShShopingCart
from shshop.module.order.models import ShShopOrderInfo, ShShopOrderSKU
from shshop.module.comments.models import ShOrderInfoComments
from shshop.module.stats.models import ShIPAddress, ShStats
from shshop.module.article.models import ShArticleCategory, ShArticle, ShArticleTags


class MenuSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShMenu
        fields = '__all__'


class PermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShPermission
        fields = '__all__'


class BannerSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShBanner
        fields = '__all__'


class UploadSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShUpload
        fields = '__all__'


class UserInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserInfo
        fields = '__all__'


class UserBalanceLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShUserBalanceLog
        fields = '__all__'


class ShopAddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShShopAddress
        fields = '__all__'


class ShopCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ShShopCategory
        fields = '__all__'


class ShopSPUSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShShopSPU
        fields = '__all__'


class ShopSpecSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShShopSpec
        fields = '__all__'


class ShopSpecOptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShShopSpecOption
        fields = '__all__'


class ShopSKUSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShShopSKU
        fields = '__all__'


class SPUCarouselSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShSPUCarousel
        fields = '__all__'


class ShopOrderInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShShopOrderInfo
        fields = '__all__'


class ShopOrderSKUSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShShopOrderSKU
        fields = '__all__'


class OrderInfoCommentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShOrderInfoComments
        fields = '__all__'


class IPAddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShIPAddress
        fields = '__all__'


class StatsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShStats
        fields = '__all__'


class ArticleCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ShArticleCategory
        fields = '__all__'


class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShArticle
        fields = '__all__'


class ArticleTagsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShArticleTags
        fields = '__all__'
