from django.shortcuts import render

from django.views.generic import ListView, DetailView
from .models import Post

class PostList(ListView):
    model = Post
    ordering = '-post_create_datetime'
    template_name = 'newslist.html'
    context_object_name = 'newslist'

class PostDetail(DetailView):
    model = Post
    template_name = 'newsdetail.html'
    context_object_name = 'newsdetail'

