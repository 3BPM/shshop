from django import forms


class CommentForm(forms.Form):
    author = forms.CharField(max_length=50)
    content = forms.CharField(widget=forms.Textarea)
    # 其他表单字段...
