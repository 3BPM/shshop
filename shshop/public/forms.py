from django import forms
from django.forms.widgets import Textarea as BaseTextarea
from django.contrib.flatpages.forms import FlatpageForm

from shshop.config.settings import sh_settings


class HTMLTextarea(BaseTextarea):
    """ 富文本编辑器 """
    template_name = "shadmin/editor.html"

    def __init__(self, attrs=None):
        super().__init__(attrs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        return context

    class Media:
        css = {'all': ('shadmin/css/style.css','shadmin/css/editor.css')}
        js = ('shadmin/js/index.js',)


class ShUploadModelForm(forms.ModelForm):
    """ 上传图片表单 """
    class Meta:
        from shshop.models import ShUpload
        model = ShUpload
        fields = ('img',)


class SearchForm(forms.Form):
    """ 搜索表单 """
    template_name = "shshop/search_form.html"

    word = forms.CharField(
        max_length=36,
        required=True,
        widget=forms.TextInput(
            {
                'type': 'search',
                'class': 'input',
                'placeholder': f'{sh_settings.SEARCH_VALUE}'
            }
        )
    )


class ShFlatpageForm(FlatpageForm):
    # 单页面应用

    class Meta(FlatpageForm.Meta):
        widgets = {
            'content': HTMLTextarea(),
        }