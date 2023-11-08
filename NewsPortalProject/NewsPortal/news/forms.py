from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['post_author', 'post_category', 'post_title', 'post_content']


