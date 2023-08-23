from django.views.generic import CreateView, ListView, View
from django.db.models import F
from django.db.utils import IntegrityError
from django.contrib import messages
from django.urls import reverse_lazy
from shshop.models import ShShopingCart, ShShopAddress
from shshop.public.mixins import (
    JsonableResponseMixin, JsonLoginRequiredMixin, JsonResponse,
    LoginRequiredMixin
)


class ShShopingCartCreateView(JsonLoginRequiredMixin, JsonableResponseMixin, CreateView):
    """ 加入购物车 """
    model = ShShopingCart
    fields = ['sku', 'num']
    success_url = reverse_lazy('shshop:carts')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        try:
            self.object = form.save()
            messages.add_message(self.request, messages.SUCCESS, f'已成功加入购物车！')
        except IntegrityError:
            carts = ShShopingCart.objects.filter(owner=self.request.user, sku=form.cleaned_data['sku'])
            carts.update(num=F('num')+int(form.cleaned_data['num']))
            self.object = carts.first()
            messages.add_message(self.request, messages.SUCCESS, f'已成功加入购物车！')
            return JsonResponse({'pk': self.object.id, 'code': 'ok', 'message': '已成功加入购物车！'}, json_dumps_params={'ensure_ascii': False})
        return super().form_valid(form)


class ShShopingCartListView(LoginRequiredMixin, ListView):

    template_name = "shshop/cart/carts.html"
    context_object_name = "carts"

    def get_queryset(self):
        queryset = ShShopingCart.objects.filter(owner=self.request.user)
        total = 0
        carts = []
        for cart in queryset:
            cart_dict = {}
            cart_dict['id'] = cart.id
            cart_dict['title'] = cart.sku.spu.title
            cart_dict['sku_id'] = cart.sku.id
            cart_dict['cover_pic'] = cart.sku.cover_pic.url
            cart_dict['options'] = list(cart.sku.options.values('name', 'spec__name'))
            cart_dict['price'] = cart.sku.price.to_eng_string()
            cart_dict['stock'] = cart.sku.stock
            cart_dict['sales'] = cart.num
            cart_dict['total_price'] = cart.num * cart.sku.price
            carts.append(cart_dict)
            total += cart.num * cart.sku.price
        return carts


class ShShopingCartUpdateView(JsonLoginRequiredMixin, View):
    """ 修改购物车数量 """

    def post(self, request, *args, **kwargs):
        cleaned_data = request.POST
        carts = ShShopingCart.objects.filter(owner=self.request.user, id=int(cleaned_data['id']))
        # 修改
        if carts.exists() and cleaned_data.get('actions') == 'update':
            carts.update(num=int(cleaned_data['num']))
            return JsonResponse({'code':'ok', 'message': '修改成功！'})
        # 删除
        elif carts.exists() and cleaned_data.get('actions') == 'delete':
            carts.delete()
            return JsonResponse({'code':'ok', 'message': '删除成功！'})
        else:
            return JsonResponse({'code':'err', 'message': '该购物不存在！'})