from django.template import Library

from shshop.public.forms import SearchForm
from shshop.models import ShPermission, ShShopCategory, ShBanner
from shshop.models import ShShopingCart, ShShopAddress
from shshop.config.settings import sh_settings


register = Library()


def sku_rate(skus):
    from django.db.models import Avg
    from shshop.models import ShOrderInfoComments, ShShopSKU
    from django.contrib.contenttypes.models import ContentType
    content_type = ContentType.objects.get_for_model(ShShopSKU)
    skus_id = skus.values_list('id', flat=True)
    comments = ShOrderInfoComments.objects.filter(
        content_type=content_type, object_id__in=list(skus_id)).aggregate(
            Avg('comment_choices')
        ).get('comment_choices__avg')

    score = comments if comments else 4.8
    return round(score, 1)


@register.simple_tag
def navbar_result():
    return ShShopCategory.get_cates()


@register.inclusion_tag(filename="shshop/banner.html")
def banners_result():
    queryset = [
        {'id': b.id, 'img': b.img.url, 'desc': b.desc, 'target_url': b.target_url }
        for b in ShBanner.objects.all()
    ]
    return {'carousels': queryset}


@register.simple_tag
def breadcrumbs(request, opts=None):
    if sh_settings.ADMIN_MENUS:
        if opts:
            p = ShPermission.objects.filter(
                permission__content_type__app_label=opts.app_label,
                permission__content_type__model=opts.model_name
            )
            request.breadcrumbs = {
                p.first().menus.name: {
                    'name': str(opts.verbose_name_plural),
                    'url': request.path
                }
            }
            return request.breadcrumbs
        return request.breadcrumbs
    else:
        return None

def spu_box_func(spu):
    def skus(spu):
        return spu.shshopsku_set.order_by('price')

    from django.db.models import Sum
    return {
        'spu': spu,
        'price': skus(spu).first().price,
        'sales': skus(spu).aggregate(Sum('sales'))['sales__sum'],
        'score': sku_rate(skus(spu))
    }

@register.inclusion_tag(filename="shshop/spu_box.html")
def spu_box(spu):
    return spu_box_func(spu)

@register.simple_tag
def search(request):
    form = SearchForm(initial=request.GET)
    return form

@register.inclusion_tag(filename="shshop/goods/page_list.html")
def page_list(request, page_obj):
    return {
        'page_obj': page_obj,
        'paginator': page_obj.paginator,
        'total': page_obj.paginator.num_pages,
        'current': request.GET.get('page', 1),
        'per_page': page_obj.paginator.per_page,
    }

@register.simple_tag
def cart_num(user):
    # 购物车商品数量
    return ShShopingCart.get_cart_count(user) if user.is_authenticated else 0


@register.inclusion_tag(filename="shshop/user/address.html")
def address_result(user):
    # 订单确认页面地址
    return {
        'address_list': list(ShShopAddress.objects.filter(owner=user).values(
            'id', 'name', 'phone', 'email', 'province', 'city', 'county', 'address', 'is_default')
        )
    }


@register.simple_tag
def order_num(orderskus):
    # 计算该订单下的订单商品数量
    # orderskus,订单关联订单商品queryset
    from django.db.models import Sum
    return orderskus.aggregate(Sum("count")).get('count__sum')


def commented_func(order):
    # 判断订单商品是否已经全部评价方法
    # order 订单对象
    commenteds = order.shshopordersku_set.values_list('is_commented', flat=True)
    return all(list(commenteds)) if commenteds else False


@register.simple_tag
def is_order_commented(order):
    return commented_func(order)


@register.inclusion_tag(filename="shshop/page.html")
def page(page_obj, next_name="Next page", pre_name="Previous", **kwargs):
    params=[]
    if kwargs:
        for k, v in kwargs.items():
            params.append(f"{k}={v}")
        params = "&".join(params)

    return {
        'page_obj': page_obj,
        'next_name': next_name,
        'pre_name': pre_name,
        'params': f"&{params}" if params else ""
    }