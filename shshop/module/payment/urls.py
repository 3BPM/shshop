from django.urls import path
from shshop.module.payment import views


urlpatterns = [
    path("", views.CashRegisterTemplateView.as_view(), name="cash_register"),
    path("paynow/", views.PayNowView.as_view(), name="pay_now"),

]