from django.urls import path
from shshop.module.post import views

urlpatterns = [
    # path("", views.ShShopingpostListView.as_view(), name="posts"),
    path("", views.POST, name="posts"),
    # path("add/", views.ShShopingpostCreateView.as_view(), name="add_post"),
    # path("update/num/", views.ShShopingpostUpdateView.as_view(), name="update_post")
]