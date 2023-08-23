from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from shshop.module.goods.models import (ShShopCategory, ShShopSPU,
                                           ShShopSpec, ShShopSpecOption,
                                           ShShopSKU, ShSPUCarousel)
from .serializers import Model1Serializer, Model2Serializer,SkuallSerializer
from rest_framework.filters import OrderingFilter
from rest_framework import mixins, viewsets
class Gooda(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = ShShopSKU.objects.all()
    serializer_class = SkuallSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ['price']

class Goods(APIView):
    def get(self, request):
        spu = ShShopSPU.objects.all()
        sku = ShShopSKU.objects.all()
        model1_serializer = Model1Serializer(spu, many=True)
        skuallSerializer=SkuallSerializer(sku, many=True)
        return Response(skuallSerializer.data)