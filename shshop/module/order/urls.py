from django.urls import path
from shshop.module.order import views

urlpatterns = [
    path("list/", views.ShshopOrderInfoListView.as_view(), name="order_list"),
    path("<int:slug>/", views.ShShopOrderInfoDetailView.as_view(), name="order_detail"),
    path("detail/<int:slug>/", views.ShShopOrderInfoUserDetailView.as_view(), name="user_order_detail")
]