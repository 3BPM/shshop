from django.urls import path
from shshop.module.user import views

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("add/address/",
         views.ShShopAddressCreateView.as_view(),
         name="add_address"),
    path("address/",
         views.ShShopAddressListView.as_view(),
         name="addrs_list"),
    path("userinfo/", views.UserInfoTemplateView.as_view(), name="userinfo"),
    path("balance/",
         views.ShUserBalanceLogTemplateView.as_view(),
         name="balance"),
]
