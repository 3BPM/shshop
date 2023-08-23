from django.urls import path
from django.contrib.sitemaps.views import sitemap

from shshop.public import views
from shshop.public.sitemaps import sitemaps


urlpatterns = [
    path("", views.HomeTemplateView.as_view(), name="home"),
    path("upload/", views.WangEditorUploadImg.as_view(), name="upload"),

    path("upload/tinymce/", views.TinymceUploadImg.as_view(), name="upload_tinymce"),

    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]
