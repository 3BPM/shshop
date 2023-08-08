from django.urls import path, include

app_name = "shshop"

urlpatterns = [
    path("", include('shshop.public.urls')),
    path("user/", include('shshop.module.user.urls')),
    path("goods/", include('shshop.module.goods.urls')),
    path("cart/", include('shshop.module.cart.urls')),
    path("post/", include('shshop.module.post.urls')),
    path("order/", include('shshop.module.order.urls')),
    path("comments/", include('shshop.module.comments.urls')),
    path("article/", include('shshop.module.article.urls')),
	path("payment/", include('shshop.module.payment.urls')),
]

