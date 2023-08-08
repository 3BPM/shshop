from rest_framework import serializers
from shshop.module.goods.models import (ShShopCategory, ShShopSPU,
                                           ShShopSpec, ShShopSpecOption,
                                           ShShopSKU, ShSPUCarousel)

class Model1Serializer(serializers.ModelSerializer):
    class Meta:
        model = ShShopSPU
        fields = ['id', 'title','category','cover_pic' ,'content','owner']

class Model2Serializer(serializers.ModelSerializer):
    class Meta:
        model = ShShopSKU
        fields = ['id', 'price', 'sales']

class SkuallSerializer(serializers.Serializer):
    spu = Model1Serializer()
    cover_pic = serializers.ImageField(   label="封面图",required=False)
    price = serializers.DecimalField(label="售价", max_digits=8, decimal_places=2)
    cost_price = serializers.DecimalField(label="成本价", max_digits=8, decimal_places=2)
    org_price = serializers.DecimalField(label="原价", max_digits=8, decimal_places=2)
    stock = serializers.IntegerField(label="库存", default=0)
    sales = serializers.IntegerField(label="销量", required=False)
    numname = serializers.CharField(label="商品成色", required=False)
    weight = serializers.FloatField(label="重量(KG)", required=False)
    vol = serializers.FloatField(label="体积(m³)", required=False)