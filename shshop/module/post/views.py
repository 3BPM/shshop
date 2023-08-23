from django.utils.datastructures import MultiValueDict
from django.views.generic import CreateView, ListView, View
from django.db.models import F
from django.db.utils import IntegrityError
from django.contrib import messages
from django.urls import reverse_lazy
from shshop.models import GoodPost
from shshop.module.goods.forms import ShShopSPUForm, ShShopSKUForm, ShSPUCarouselForm
from shshop.module.goods.models import ShShopSpecOption, ShShopCategory, User
from shshop.public.mixins import (
    JsonableResponseMixin, JsonLoginRequiredMixin, JsonResponse,
    LoginRequiredMixin
)
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from shshop.models import ShShopSPU, ShShopSKU, ShSPUCarousel

from django.http import QueryDict

class ShShopSPUCreateView(CreateView):
    model = ShShopSPU
    fields = ['title', 'keywords', 'desc', 'category', 'unit', 'cover_pic',
              'freight', 'content']
    success_url = reverse_lazy('shshop:spu_list')#success_url被设置为 shshop:spu_list的反向解析结果，意味着它将生成名为shshop:spu_list的URL
    template_name = 'shshop/post/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sku_form'] = ShShopSKUForm()
        context['carousel_form'] = ShSPUCarouselForm()
        context['spu_form'] = ShShopSPUForm()
        return context

    def form_valid(self, form):
        print(self.request)
        print(form)#TODO 需要拆分
        # spu = form.save(commit=False)
        # spu.owner = self.request.user
        # spu.save()
        #
        # # Create SKU and its options
        # sku_form = ShShopSKUForm(self.request.POST, self.request.FILES)#TODO 有多个时需要单独处理
        # if sku_form.is_valid():
        #     sku = sku_form.save(commit=False)
        #     sku.spu = spu
        #     sku.cover_pic = spu.cover_pic
        #     sku.save()
        #     sku_form.save_m2m()  # Save related options
        #
        # # Create carousel
        # carousel_form = ShSPUCarouselForm(self.request.POST, self.request.FILES)#TODO 有多个时需要单独处理
        # if carousel_form.is_valid():
        #     carousel = carousel_form.save(commit=False)
        #     carousel.product = spu
        #     carousel.img = spu.cover_pic
        #     carousel.save()

        return redirect(self.success_url)


# class ShShopingpostCreateView(JsonLoginRequiredMixin, JsonableResponseMixin, CreateView):
#     """ 加入购物车 """
#     model = GoodPost
#     fields = ['sku', 'num']
#     success_url = reverse_lazy('shshop:posts')

#     def form_valid(self, form):
#         form.instance.owner = self.request.user
#         try:
#             self.object = form.save()
#             messages.add_message(self.request, messages.SUCCESS, f'已成功加入购物车！')
#         except IntegrityError:
#             posts = GoodPost.objects.filter(owner=self.request.user, sku=form.cleaned_data['sku'])
#             posts.update(num=F('num')+int(form.cleaned_data['num']))
#             self.object = posts.first()
#             messages.add_message(self.request, messages.SUCCESS, f'已成功加入购物车！')
#             return JsonResponse({'pk': self.object.id, 'code': 'ok', 'message': '已成功加入购物车！'}, json_dumps_params={'ensure_ascii': False})
#         return super().form_valid(form)


class ShShopingpostListView(LoginRequiredMixin, ListView):

    template_name = "shshop/post/posts.html"
    context_object_name = "posts"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        form = ShShopSPUForm()
        context['form'] = form
        context['option'] = ShShopSpecOption.objects.all()
        return context

    def get_queryset(self):
        queryset = []#GoodPost.objects.filter(owner=self.request.user)
        total = 0
        posts = []
#         for post in queryset:
#             post_dict = {}
#             post_dict['id'] = post.id
#             post_dict['title'] = post.sku.spu.title
#             post_dict['sku_id'] = post.sku.id
#             post_dict['cover_pic'] = post.sku.cover_pic.url
#             post_dict['options'] = list(post.sku.options.values('name', 'spec__name'))
#             post_dict['price'] = post.sku.price.to_eng_string()
#             post_dict['stock'] = post.sku.stock
#             post_dict['sales'] = post.num
#             post_dict['total_price'] = post.num * post.sku.price
#             posts.append(post_dict)
#             total += post.num * post.sku.price
        return posts



from django.db import transaction

@transaction.atomic
def POST(request):
    template_name = 'shshop/post/create.html'
    context = {}
    context['sku_form'] = ShShopSKUForm()
    context['carousel_form'] = ShSPUCarouselForm()
    context['spu_form'] = ShShopSPUForm()
    context['categories'] = ShShopCategory.objects.all()
    context['spec_options'] = ShShopSpecOption.objects.all()

    if request.method=="POST":
        print(request.POST)
        print(request.FILES)
        skus=request.POST.get('skus').split(',')
        carousels=request.POST.get('carousels').split(',')
        print(skus)
        print(carousels)

        #SPU
        owner = User.objects.get(pk=request.user.pk)
        spuForm=ShShopSPUForm(request.POST, request.FILES,owner=owner)
        # print(spuForm)
        if spuForm.is_valid():
            #商品信息保存
            spu = spuForm.save()
            categories = request.POST.getlist('category')
            cates = [ShShopCategory.objects.get(id=c) for c in categories]
            spu.category.set(cates)
            spu.save()
            print(spu.id)
        else:
            print('spu数据出错')
            return render(request,template_name=template_name,context=context)

        #SKU
        skus=request.POST.get('skus').split(',')

        for i in skus:
            skuData = QueryDict('', mutable=True)
            n=request.POST.get(f'numname{i}')
            if n=='':
                n='0'
            w=request.POST.get(f'weight{i}')
            if w=='':
                w='0'
            v=request.POST.get(f'vol{i}')
            if v=='':
                v='0'
            skuData.update({
                'spu': spu,
                # 'options': request.POST.get(f'option{i}'),
                'price': request.POST.get(f'price{i}'),
                'cost_price': request.POST.get(f'cost_price{i}'),
                'org_price': request.POST.get(f'org_price{i}'),
                'stock': request.POST.get(f'stock{i}'),
                'numname': n,
                'weight': w,
                'vol': v,
            })
            fileDict = MultiValueDict({'cover_pic': request.FILES.getlist(f'cover{i}')})
            print(skuData,fileDict)
            skuForm=ShShopSKUForm(skuData,fileDict,spu=spu)
            print(skuForm)
            if skuForm.is_valid():
                sku = skuForm.save()
                options = request.POST.getlist(f'option{i}')
                opts = [ShShopSpecOption.objects.get(id=o) for o in options]
                sku.options.set(opts)
                sku.save()
            else:
                print('sku数据出错',skuForm.errors)
                return render(request, template_name=template_name, context=context)

        #carousel
        carousels=request.POST.get('carousels').split(',')
        for i in carousels:
            carouselsData = QueryDict('', mutable=True)
            carouselsData.update({
                'product': spu,
            })
            fileDict = MultiValueDict({'img': request.FILES.getlist(f'img_{i}')})
            carouselsForm = ShSPUCarouselForm(carouselsData,fileDict,spu=spu)
            if carouselsForm.is_valid():
                carouselsForm.save()
            else:
                print('carousel数据出错',carouselsForm.errors)
                return render(request, template_name=template_name, context=context)
        return redirect(f'/goods/spu/{spu.id}/')

    else:
        return render(request,template_name=template_name,context=context)