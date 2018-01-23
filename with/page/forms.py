from django import forms
from ckeditor_uploader.fields import RichTextUploadingFormField
from .models import Category

__all__ = [
    'CommentForm',
    'ReplyForm',
    'ArticleForm',
]


class CommentForm(forms.Form):
    content = forms.CharField(required=True, max_length=200)


class ReplyForm(forms.Form):
    content = forms.CharField(required=True, max_length=200)


class ArticleForm(forms.Form):
    name = forms.CharField(label='文章名称', required=True,
                           widget=forms.TextInput(attrs={'style': 'border:1px solid #ccc;width:80%;'}))
    image = forms.ImageField(label='图片', required=True)
    category = forms.ChoiceField(required=True, label="分类")
    content = RichTextUploadingFormField(label='内容', config_name="basic")
