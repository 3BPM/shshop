from django.urls import path
from shshop.module.cart import views

urlpatterns = [
    path("", views.ShShopingCartListView.as_view(), name="carts"),
    path("add/", views.ShShopingCartCreateView.as_view(), name="add_cart"),
    path("update/num/", views.ShShopingCartUpdateView.as_view(), name="update_cart")
]