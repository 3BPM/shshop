from django import forms
from shshop.models import ShShopSPU
from shshop.module.goods.models import (
    ShShopSKU,
    ShSPUCarousel,
    ShShopSpecOption,
    ShShopCategory,
)
from shshop.public.forms import HTMLTextarea


class ShShopSPUForm(forms.ModelForm):
    # 商品表单

    title = forms.CharField(
        label="商品名称",
        widget=forms.TextInput(
            attrs={"autofocus": True, "class": "input", "placeholder": " 请输入商品名称..."}
        ),
    )
    keywords = forms.CharField(
        label="商品关键词", widget=forms.TextInput(attrs={"class": "input"})
    )
    desc = forms.CharField(
        label="商品描述", widget=forms.TextInput(attrs={"class": "input"})
    )
    ops = []
    # category = forms.CharField(widget=forms.CheckboxSelectMultiple(choices=ops))
    unit = forms.CharField(label="单位", widget=forms.TextInput(attrs={"class": "input"}))
    cover_pic = forms.ImageField(
        label="封面图",
        widget=forms.FileInput(attrs={"class": "input", "accept": "image/*"}),
    )
    freight = forms.CharField(
        label="运费", widget=forms.NumberInput(attrs={"class": "input", "value": "0"})
    )
    # content = forms.CharField(label='商品详情',widget=HTMLTextarea())
    owner = forms.CharField(
        label="用户", widget=forms.HiddenInput(attrs={"class": "input", "value": "1"})
    )

    class Meta:
        model = ShShopSPU
        # fields = ('title','keywords',)
        fields = (
            "title",
            "keywords",
            "desc",
            "category",
            "unit",
            "cover_pic",
            "freight",
            "content",
            "owner",
        )
        widgets = {
            "content": HTMLTextarea(),
        }

    def __init__(self, *args, **kwargs):
        self.owner = kwargs.pop("owner", None)
        super().__init__(*args, **kwargs)
        self.ops = self.get_ops()

    def get_ops(self):
        ops = []
        ops = [(s.id, s.name) for s in ShShopCategory.objects.all()]
        return ops

    # def save(self, commit=True):
    #     instance = super().save(commit=False)
    #     instance.owner=self.request.user
    #     if commit:
    #         instance.save()
    #     return instance

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data["owner"] = self.owner

        return cleaned_data


class ShShopSKUForm(forms.ModelForm):
    # 规格表单
    spu = forms.CharField(
        label="商品", widget=forms.HiddenInput(attrs={"class": "input", "value": "1"})
    )
    ops = []

    # options = forms.CharField(label='发布区域',widget=forms.RadioSelect(choices=ops,
    #     attrs={"class":""
    #    }))
    cover_pic = forms.ImageField(
        label="封面图",
        widget=forms.FileInput(attrs={"class": "input", "accept": "image/*"}),
    )
    price = forms.CharField(
        label="售价",
        widget=forms.NumberInput(
            attrs={
                "class": "input inline-input",
            }
        ),
    )
    cost_price = forms.CharField(
        label="成本",
        widget=forms.NumberInput(
            attrs={
                "class": "input inline-input",
            }
        ),
    )
    org_price = forms.CharField(
        label="原价",
        widget=forms.NumberInput(
            attrs={
                "class": "input inline-input",
            }
        ),
    )
    stock = forms.CharField(
        label="库存",
        widget=forms.NumberInput(
            attrs={
                "class": "input inline-input",
            }
        ),
    )
    numname = forms.CharField(
        label="商品成色",
        widget=forms.TextInput(
            attrs={
                "class": "input inline-input",
            }
        ),
    )
    weight = forms.CharField(
        label="重量(KG)",
        widget=forms.NumberInput(
            attrs={
                "class": "input inline-input",
            }
        ),
    )
    vol = forms.CharField(
        label="体积(m³)",
        widget=forms.NumberInput(
            attrs={
                "class": "input inline-input",
            }
        ),
    )

    class Meta:
        model = ShShopSKU
        fields = (
            "spu",
            "options",
            "cover_pic",
            "price",
            "cost_price",
            "org_price",
            "stock",
            "numname",
            "weight",
            "vol",
        )

    def __init__(self, *args, **kwargs):
        self.spu = kwargs.pop("spu", None)
        super().__init__(*args, **kwargs)
        self.ops = self.get_ops()

    def get_ops(self):
        ops = []
        ops = [(s.id, s.name) for s in ShShopSpecOption.objects.all()]
        return ops

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data["spu"] = self.spu

        return cleaned_data


class ShSPUCarouselForm(forms.ModelForm):
    # 轮播图表单
    product = forms.CharField(
        label="商品", widget=forms.HiddenInput(attrs={"class": "input", "value": "1"})
    )
    img = forms.ImageField(
        label="轮播图",
        widget=forms.FileInput(attrs={"class": "input", "accept": "image/*"}),
    )

    class Meta:
        model = ShSPUCarousel
        fields = ("img", "product")

    def __init__(self, *args, **kwargs):
        self.spu = kwargs.pop("spu", None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data["product"] = self.spu
