from shshop.models import *
from rest_framework import generics
from .serializers import *
class MenuList(generics.ListCreateAPIView):
    queryset = ShMenu.objects.all()
    serializer_class = MenuSerializer


class PermissionList(generics.ListCreateAPIView):
    queryset = ShPermission.objects.all()
    serializer_class = PermissionSerializer


class BannerList(generics.ListCreateAPIView):
    queryset = ShBanner.objects.all()
    serializer_class = BannerSerializer


class UploadList(generics.ListCreateAPIView):
    queryset = ShUpload.objects.all()
    serializer_class = UploadSerializer


class UserInfoList(generics.ListCreateAPIView):
    # queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer
    def get_queryset(self):
        queryset = UserInfo.objects.all()
        owner = self.request.query_params.get('owner', None)
        if owner is not None:
            queryset = queryset.filter(owner=owner)
        return queryset



class UserBalanceLogList(generics.ListCreateAPIView):
    queryset = ShUserBalanceLog.objects.all()
    serializer_class = UserBalanceLogSerializer


class ShopAddressList(generics.ListCreateAPIView):
    queryset = ShShopAddress.objects.all()
    serializer_class = ShopAddressSerializer


class ShopCategoryList(generics.ListCreateAPIView):
    queryset = ShShopCategory.objects.all()
    serializer_class = ShopCategorySerializer


class ShopSPUList(generics.ListCreateAPIView):
    serializer_class = ShopSPUSerializer
    def get_queryset(self):
        queryset = ShShopSPU.objects.all()
        var = self.request.query_params.get('uid', None)
        if var is not None:
            queryset = queryset.filter(owner=var)
        return queryset
class ShopSPUCList(generics.ListCreateAPIView):
    serializer_class = ShopSPUSerializer
    def get_queryset(self):
        queryset = ShShopSPU.objects.all()
        var = self.request.query_params.get('ctg', None)
        if var is not None:
            queryset = queryset.filter(category=var)
        return queryset


class ShopSpecList(generics.ListCreateAPIView):
    queryset = ShShopSpec.objects.all()
    serializer_class = ShopSpecSerializer


class ShopSpecOptionList(generics.ListCreateAPIView):
    queryset = ShShopSpecOption.objects.all()
    serializer_class = ShopSpecOptionSerializer


class ShopSKUList(generics.ListCreateAPIView):
    serializer_class = ShopSKUSerializer
    def get_queryset(self):
        queryset = ShShopSKU.objects.all()
        var = self.request.query_params.get('spu', None)
        if var is not None:
            queryset = queryset.filter(spu=var)
        return queryset

class SPUCarouselList(generics.ListCreateAPIView):
    queryset = ShSPUCarousel.objects.all()
    serializer_class = SPUCarouselSerializer


class ShopOrderInfoList(generics.ListCreateAPIView):
    serializer_class = ShopOrderInfoSerializer
    def get_queryset(self):
        queryset = ShShopOrderInfo.objects.all()
        var = self.request.query_params.get('owner', None)
        if var is not None:
            queryset = queryset.filter(owner=var)
        return queryset

class ShoppingCart(generics.ListCreateAPIView):
    queryset = ShShopingCart.objects.all()
    serializer_class = ShopOrderInfoSerializer


class ShopOrderSKUList(generics.ListCreateAPIView):
    queryset = ShShopOrderSKU.objects.all()
    serializer_class = ShopOrderSKUSerializer


class OrderInfoCommentsList(generics.ListCreateAPIView):
    queryset = ShOrderInfoComments.objects.all()
    serializer_class = OrderInfoCommentsSerializer


class IPAddressList(generics.ListCreateAPIView):
    queryset = ShIPAddress.objects.all()
    serializer_class = IPAddressSerializer


class StatsList(generics.ListCreateAPIView):
    queryset = ShStats.objects.all()
    serializer_class = StatsSerializer


class ArticleCategoryList(generics.ListCreateAPIView):
    queryset = ShArticleCategory.objects.all()
    serializer_class = ArticleCategorySerializer


class ArticleList(generics.ListCreateAPIView):
    queryset = ShArticle.objects.all()
    serializer_class = ArticleSerializer


class ArticleTagsList(generics.ListCreateAPIView):
    queryset = ShArticleTags.objects.all()
    serializer_class = ArticleTagsSerializer
