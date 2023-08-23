from django.views.generic import TemplateView, View
from django.urls import reverse
from django.core.cache import cache
from django.db.models import F

from shshop.public.mixins import LoginRequiredMixin, JsonResponse, JsonLoginRequiredMixin
from shshop.models import (ShShopingCart, ShShopSKU,
                              ShShopOrderInfo, ShShopAddress,
                              ShShopOrderSKU, ShUserBalanceLog, UserInfo)


class CashRegisterTemplateView(LoginRequiredMixin, TemplateView):
    """ 收银台 """
    template_name = "shshop/payment/cash_register.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['carts'] = self.get_carts()
        if context['carts']:
            context['count'] = self.get_count(context['carts'])
            context['total'] = self.get_total(context['carts'])
            context['freight'] = self.get_freight(context['carts'])
            context['pay_total'] = self.get_pay_total(context['carts'])
        return context

    def get_carts(self):
        cleaned_data = self.request.GET.dict()
        carts = []
        if cleaned_data and cleaned_data.get('cartsID'):
            carts_ids = [
                int(id) for id in cleaned_data.get('cartsID').split(',')
            ]
            carts = ShShopingCart.objects.filter(id__in=carts_ids)
            for cart in carts:
                cart.type = 'cart'
                cart.total_price = cart.sku.price * cart.num
                # 粗略计算运费, 运费为固定，仅与sku有关
                cart.freight = 0
                cart.freight += cart.sku.spu.freight
        elif cleaned_data and cleaned_data.get('skuID'):
            carts = ShShopSKU.objects.filter(
                id=int(cleaned_data.get('skuID')))
            for cart in carts:
                cart.type = 'sku'
                cart.num = int(cleaned_data.get('num'))
                cart.total_price = cart.price * cart.num
                # 粗略计算运费
                cart.freight = cart.spu.freight
        # 缓存订单信息
        cache.set(f'carts{self.request.user.id}', carts, None)
        return carts

    def get_count(self, carts):
        # 商品总数
        cleaned_data = self.request.GET.dict()
        count = 0
        if cleaned_data and cleaned_data.get('skuID'):
            count = int(cleaned_data.get('num'))
        elif cleaned_data and cleaned_data.get('cartsID'):
            from django.db.models import Sum
            count = carts.aggregate(Sum('num'))['num__sum']
        return count

    def get_total(self, carts):
        # 获取商品总价，不含运费
        total = 0
        for cart in carts:
            total += cart.total_price
        return total

    def get_freight(self, carts):
        # 获取运费
        freight = 0
        for cart in carts:
            freight += cart.freight
        return freight

    def get_pay_total(self, carts):
        # 实际支付金额，含运费
        return self.get_total(carts) + self.get_freight(carts)

    def generate_order_sn(self):
        # 当前时间 + userid + 随机数
        import time
        from random import Random
        random_ins = Random()
        order_sn = "{time_str}{user_id}{ranstr}".format(
            time_str=time.strftime("%Y%m%d%H%M%S"),
            user_id=self.request.user.id,
            ranstr=random_ins.randint(10, 99))
        return order_sn

    def post(self, request, *args, **kwargs):
        cleaned_data = request.POST.dict()

        # 收货地址验证
        if not cleaned_data.get('addr_id'):
            return JsonResponse({'code': 'err', 'message': '收货地址不能为空！'})
        try:
            addr = ShShopAddress.objects.get(
                id=int(cleaned_data['addr_id']))
        except ShShopAddress.DoesNotExist:
            return JsonResponse({'code': 'err', 'message': '收货地址无效！'})

        # 缓存中的订单数据是否存在
        carts = cache.get(f'carts{self.request.user.id}')
        if not carts:
            return JsonResponse({'code': 'err', 'message': '订单过期，请刷新重试！'})

        datas = {
            "owner": request.user,
            "order_sn": self.generate_order_sn(),
            "pay_status": 1,
            "total_amount": self.get_pay_total(carts),
            "order_mark": cleaned_data.get('order_mark', ''),
            "name": addr.name,
            "phone": addr.phone,
            "email": addr.email,
            "address": f"{addr.province}{addr.city}{addr.county}{addr.address}"
        }

        # 创建订单
        orderinfo = ShShopOrderInfo.objects.create(**datas)

        # 创建订单商品
        for cart in carts:
            # 订单商品保存
            sku = cart if cart.type == 'sku' else cart.sku
            spec = ','.join([
                f"{op.spec.name}:{op.name}" for op in sku.options.all() if op
            ])
            ShShopOrderSKU.objects.create(order=orderinfo,
                                             sku=sku,
                                             title=sku.spu.title,
                                             desc=sku.spu.desc,
                                             spec=spec,
                                             content=sku.spu.content,
                                             count=cart.num,
                                             price=sku.price)

            # 加销量 减库存
            ShShopSKU.objects.filter(id=sku.id).update(
                stock=F('stock') - int(cart.num),
                sales=F('sales') + int(cart.num))

            # 清理购物车
            if cart.type == 'cart':
                cart.delete()

            # 清理缓存
            cache.delete('carts')

        pay_url = reverse("shshop:order_detail", args=[orderinfo.order_sn])
        return JsonResponse({
            'code': 'ok',
            'message': 'ok',
            'pay_url': pay_url
        })


class PayNowView(JsonLoginRequiredMixin, View):
    """ 收款 """

    def post(self, request, *args, **kwargs):
        cleaned_data = request.POST.dict()
        if (not cleaned_data) or (cleaned_data.get('order_sn')
                                  is None) or (cleaned_data.get('paymethod')
                                               is None):
            return JsonResponse({
                'code': 'err',
                'message': '未获取到任何订单信息或支付信息有误！'
            })

        code = ""
        message = ""

        order_sn = cleaned_data['order_sn']
        paymethod = cleaned_data['paymethod']
        try:
            userinfo = request.user.userinfo
            order = ShShopOrderInfo.objects.filter(
                owner=request.user, order_sn=order_sn).first()

            # 余额支付
            if order and int(paymethod) == 4:
                from django.utils import timezone
                # 余额存量判断
                if userinfo.balance < order.total_amount:
                    return JsonResponse({'code': 'err', 'message': '余额不足！'})

                # 扣除余额
                UserInfo.objects.filter(owner=request.user).update(
                    balance=F('balance') - order.total_amount)
                # 修改订单信息
                order.pay_status = 2
                order.trade_sn = f"YE{order_sn}"
                order.pay_method = 4
                order.pay_time = timezone.now()
                order.save()

                # 记录余额变动日志
                ShUserBalanceLog.objects.create(owner=request.user,
                                                   amount=order.total_amount,
                                                   change_status=2,
                                                   change_way=3)
                # 返回支付结果页
                code = "ok",
                message = "支付地址返回成功！"
                kwargs[
                    'pay_url'] = f"{reverse('shshop:order_detail', args=[order.order_sn])}"
            else:
                code = "err"
                message = "暂不支持该支付方式"

            context = {"code": code, "message": message, **kwargs}

            return JsonResponse(context)
        except UserInfo.DoesNotExist:
            return JsonResponse({
                "code": "err",
                "message": "该用户信息不完整，请前往个人中心补充！",
                **kwargs
            })
