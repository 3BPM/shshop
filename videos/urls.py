from django.urls import path
from . import views

app_name = "videos"

urlpatterns = [
    path("", views.video_list, name="video_list"),
    path("video/<int:video_id>/", views.video_detail, name="video_detail"),
    path("video/<int:video_id>/edit/", views.video_edit, name="video_edit"),
    path("video/<int:video_id>/comments/", views.add_comment, name="add_comment"),
]
