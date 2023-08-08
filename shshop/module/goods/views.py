from django.db.models import Q
from django.views.generic.detail import SingleObjectMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView

from shshop.config.settings import sh_settings
from shshop.models import (
    ShShopSPU, ShShopSKU, ShShopCategory, ShShopSpecOption,
    ShOrderInfoComments
)
from shshop.public.forms import SearchForm


class ShShopSPUListView(ListView):
    """ 全部商品 """
    template_name = "shshop/goods/spus_list.html"
    paginate_by = sh_settings.GOODS_PAGINATE_BY
    paginate_orphans = sh_settings.GOODS_PAGINATE_ORPHANS

    def get_queryset(self):
        params = self.request.GET.dict()
        # 默认按日期排序
        queryset = ShShopSPU.objects.order_by('-add_date')
        # 按销量或价格排序
        if self.get_params_filed(params):
            queryset = self.get_order_queryset(self.get_params_filed(params), spus=queryset)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cates'] = ShShopCategory.get_cates().order_by('-add_date')
        context['sub_cates'] = context['cates'].first().shshopcategory_set.all() if context['cates'].first() else []
        context['params'] = self.request.GET.dict()
        return context

    def get_order_queryset(self, params, spus, filter={}):
        # 按销量或价格排序
        queryset = []
        # 按价格排序
        if params and params['order'].replace('-', '') == 'price':
            skus = ShShopSKU.objects.filter(**filter).order_by(*list(params.values()))
            for sku in skus:
                if sku.spu not in queryset:
                    queryset.append(sku.spu)
        # 按销量排序
        elif params and params['order'].replace('-', '') == 'sales':
            from django.db.models import Sum
            datas = [{'spu': spu, 'sales': spu.shshopsku_set.aggregate(Sum('sales'))['sales__sum']} for spu in spus if spu]
            order_reverse = True if params['order'] == '-sales' else False
            datas.sort(key=lambda s: s['sales'], reverse=order_reverse)
            queryset = [ data['spu'] for data in datas ]
        return queryset

    def get_params_filed(self, params):
        if params.get('order'):
            return {'order':params.get('order')}
        return None


class ShShopCategoryDetailView(SingleObjectMixin, ShShopSPUListView):
    """ 商品分类 """
    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=ShShopCategory.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cate_obj'] = self.object
        context['sub_cates'] = self.get_sub_cates()
        return context

    def get_queryset(self):
        cate = self.object
        params = self.request.GET.dict()
        if cate.parent is None:
            spus = ShShopSPU.objects.filter(category__in=cate.shshopcategory_set.all()).order_by('-add_date').distinct()
            # 按销量或价格排序
            if self.get_params_filed(params):
                cates = cate.shshopcategory_set.all()
                spus = self.get_order_queryset(self.get_params_filed(params), spus=spus, filter={'spu__category__in': cates})
        else:
            spus = ShShopSPU.objects.filter(category__id=self.kwargs['pk']).order_by('-add_date')
            # 按销量或价格排序
            if self.get_params_filed(params):
                spus = self.get_order_queryset(self.get_params_filed(params), spus=spus, filter={'spu__category__id':self.kwargs['pk']})
        return spus

    def get_sub_cates(self):
        if self.object.parent:
            return self.object.parent.shshopcategory_set.all()
        elif self.object.parent is None:
            return self.object.shshopcategory_set.all()


class SearchTemplateView(ShShopSPUListView):
    """ 搜索视图 """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['word'] = self.request.GET.get('word')
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        form = SearchForm(self.request.GET)
        if form.is_valid():
            word = form.cleaned_data['word']
            queryset = queryset.filter(
                Q(title__icontains=word)|Q(desc__icontains=word)|Q(keywords__icontains=word)
            )
            messages.add_message(self.request, messages.SUCCESS, f'共搜索到{queryset.count()}条数据')
        return queryset


class ShShopSPUDetailView(DetailView):
    """ 商品详情页 """
    model = ShShopSPU
    template_name = "shshop/goods/spu_detail.html"
    context_object_name = "spu"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['skus'], context['specs'], context['current_ops'] = self.get_skus()
        context['tabs_active'] = self.request.GET.get('tabsActive', 'content')
        context['page_comments'] = self.get_comments_page()
        context['like_rate'], context['score'] = self.get_good_rate()
        context['hot_spus'] = ShShopSPU.get_hots()

        from shshop.module.stats.views import ShStatsMixins
        stats = ShStatsMixins(self.request)
        context['stats'] = stats.get_stats(self.model, self.get_object().id)
        return context

    def get_banners(self, sku_id=None):
        # 轮播图
        spu = self.get_object()
        banners = [ban.img.url for ban in spu.shspucarousel_set.all()]
        if sku_id is not None:
            try:
                sku = ShShopSKU.objects.get(id=sku_id)
                if sku.cover_pic:
                    banners.insert(0, sku.cover_pic.url)
            except ShShopSKU.DoesNotExist:
                pass
        return banners

    def get_skus(self):
        # 规格商品
        spu = self.get_object()
        skus_queryset = spu.shshopsku_set.order_by('price')

        # 当前spu下的规格选项
        specs = []
        # 规格选项对应的sku
        skus = {}
        for sku in skus_queryset:
            sku_options_names = sku.options.values_list('name', flat=True)
            options = ','.join(sku_options_names)
            skus[options] = {
                'sku_id': sku.id,
                'price': sku.price.to_eng_string(),
                'org_price': sku.org_price.to_eng_string(),
                'stock': sku.stock,
                'sales': sku.sales,
                'cover_pic': sku.cover_pic.url if sku.cover_pic else spu.cover_pic.url,
                'banners': self.get_banners(sku_id=sku.id)
            }

            # 返回当前spu下的specs
            for op in sku.options.all():
                spec_dict = {
                    'spec': op.spec.name,
                    'options': list(
                        ShShopSpecOption.objects.filter(
                            spec=op.spec
                            ).values_list('name', flat=True)
                        )
                }
                # 防止重复加入
                if spec_dict not in specs:
                    specs.append(spec_dict)
        # 默认规格
        current_ops = ''
        if skus_queryset.first():
            current_ops = list(skus_queryset.first().options.values_list('name', flat=True))
        return skus, specs, current_ops

    def get_comments(self):
        # 评价列表
        from django.contrib.contenttypes.models import ContentType
        content_type = ContentType.objects.get_for_model(ShShopSKU)
        skus_id = self.get_object().shshopsku_set.values_list('id', flat=True)
        comments = ShOrderInfoComments.objects.filter(content_type=content_type, object_id__in=list(skus_id))
        return comments

    def get_comments_page(self):
        # 留言分页
        from django.core.paginator import Paginator
        paginator = Paginator(self.get_comments(), 5)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return page_obj

    def get_good_rate(self):
        # 评分及满意度
        comments = self.get_comments()
        # 总评价数
        rates = comments.count()
        # 大于等于3分的人数
        rate_gte_3 = comments.filter(comment_choices__gte=3).count()
        # 满意度,大于三分的占比数
        like_rate = (rate_gte_3 / rates) * 100 if rates else 98
        # 评分
        from django.db.models import Avg
        s = comments.aggregate(Avg('comment_choices')).get('comment_choices__avg')
        score = s if s else 4.8
        return round(like_rate), round(score, 1)