from django.urls import path
from shshop.module.article import views

urlpatterns = [
    path("", views.ShArticleListView.as_view(), name="article_list"),
    path("<int:pk>/", views.ShArticleDetailView.as_view(), name="article_detail"),
    path('cate/<int:pk>/', views.ShArticleCategoryListView.as_view(), name='article_category_list'),
]