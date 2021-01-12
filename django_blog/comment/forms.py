from django import forms

from .models import Comment

import mistune

class CommentForm(forms.ModelForm):
    nickname = forms.CharField(
        label="昵称",
        max_length=50,
        widget=forms.widgets.Input(
            attrs={'class': 'form-control', 'style': 'width:60%'}
        )
    )
    email = forms.CharField(
        label="邮箱",
        max_length=50,
        widget=forms.widgets.EmailInput(
            attrs={'class': 'form-control', 'style': 'width:60%'}
        )
    )
    website = forms.CharField(
        label="网站",
        max_length=50,
        widget=forms.widgets.URLInput(
            attrs={'class': 'form-control', 'style': 'width:60%'}
        )
    )
    context = forms.CharField(
        label="评论内容",
        max_length=500,
        widget=forms.widgets.Textarea(
            attrs={'class': 'form-control', 'rows': 6, 'cols': 60}
        )
    )

    def clean_context(self):
        # cleaned_data就是读取表单返回的值，返回类型为字典dict型
        context = self.cleaned_data.get("context")
        if len(context) < 10:
            raise forms.ValidationError("评论内容太短了")
        context = mistune.markdown(context)
        return context

    class Meta:
        model = Comment
        fields = ("nickname", "email", "website", "context")