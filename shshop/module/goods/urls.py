from django.urls import path
from shshop.module.goods import views

urlpatterns = [
    path("", views.ShShopSPUListView.as_view(), name="spus"),
    path("cate/<int:pk>/", views.ShShopCategoryDetailView.as_view(), name="cate_detail"),
    path("search/", views.SearchTemplateView.as_view(), name="search"),
    path("spu/<int:pk>/", views.ShShopSPUDetailView.as_view(), name="spu_detail"),
]