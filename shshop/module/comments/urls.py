from django.urls import path
from shshop.module.comments import views


urlpatterns = [
    path("<int:slug>/form/", views.ShOrderInfoCommentsFormView.as_view(), name="comments_create")
]
