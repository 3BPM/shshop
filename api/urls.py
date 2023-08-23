from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *
from rest_framework.urlpatterns import format_suffix_patterns
from .auth.views import CustomAuthToken, RegisterView, UserAvatarUpdateView
from .auth.user import UserInfoMenmberViewset,ShShopAddressViewSet
from .goods.views import Gooda,Goods
router = DefaultRouter()
router.register('usermember', UserInfoMenmberViewset, basename='user')
router.register('useraddress', ShShopAddressViewSet, basename='address')
router.register(r'goods', Gooda, basename='goodsviewset')


urlpatterns = [
    path('public/menu/', MenuList.as_view(), name='menu'),
    path('public/permission/', PermissionList.as_view(), name='permission'),
    path('public/banner/', BannerList.as_view(), name='banner'),
    path('public/upload/', UploadList.as_view(), name='upload'),
    path('user/info/', UserInfoList.as_view(), name='userinfo'),
    path('user/balance/log/', UserBalanceLogList.as_view(), name='userbalancelog'),
    path('user/shop/address/', ShopAddressList.as_view(), name='shopaddress'),
    path('goods/category/', ShopCategoryList.as_view(), name='shopcategory'),
    path('goods/cspu/', ShopSPUCList.as_view(), name='shopspu'),#可查找分类 ?ctg= 如http://116.63.12.26/api/goods/cspu/?ctg=8
    path('goods/spu/', ShopSPUList.as_view(), name='shopspu'),#可查找owner ?uid=
    path('goods/spec/', ShopSpecList.as_view(), name='shopspec'),
    path('goods/spec/option/', ShopSpecOptionList.as_view(), name='shopspecoption'),
    path('goods/sku/', ShopSKUList.as_view(), name='shopsku'), #可查找spu ?spu=

    path('goods/spu/carousel/', SPUCarouselList.as_view(), name='spucarousel'),
    path('cart/shoppingcart/', ShoppingCart.as_view(), name='shoppingcart'),
    path('order/info/', ShopOrderInfoList.as_view(), name='shoporderinfo'),
    path('order/sku/', ShopOrderSKUList.as_view(), name='shopordersku'),
    path('comments/orderinfo/', OrderInfoCommentsList.as_view(), name='orderinfocomments'),
    path('goodskuspu/',Goods.as_view(),name='goods'),
    path("auth/login/",CustomAuthToken.as_view(),name='authtoken'),
    path("auth/signup/",RegisterView.as_view(),name='register'),
    path("auth/upimg/",UserAvatarUpdateView.as_view(),name='upimg'),
    path("auth/article/",ArticleList.as_view(),name='article'),

]

urlpatterns = format_suffix_patterns(urlpatterns)
