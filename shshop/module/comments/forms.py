from django import forms

from shshop.models import ShOrderInfoComments


class ShOrderInfoCommentsModelForm(forms.ModelForm):

    class Meta:
        model = ShOrderInfoComments
        fields = ('content', 'comment_choices', 'object_id')
        widgets = {
            'content': forms.Textarea(attrs={"class":"textarea","rows": 5,  "placeholder":"请如实发表您对该商品的感受..."}),
        }
