from django.shortcuts import render

from django.urls import reverse_lazy
from django.urls import reverse

from django.views.generic import ListView, DetailView,  CreateView, UpdateView, DeleteView


from .models import Author, Post, Category
from .forms import PostForm
from .filters import PostFilter, FilterSet


class PostList(ListView):
    model = Post
    ordering = '-post_create_datetime'
    template_name = 'newslist.html'
    context_object_name = 'newslist'
    paginate_by = 10


class PostDetail(DetailView):
    model = Post
    template_name = 'newsdetail.html'
    context_object_name = 'newsdetail'


class PostSearch(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'search'
    ordering = ['-post_create_datetime']
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'create.html'
    context_object_name = 'create'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        if 'article' in self.request.path:
            post.post_type = 'AR'
        elif 'news/create/' in self.request.path:
            post.post_type = 'NW'
        post.save()
        return super().form_valid(form)


class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'edit.html'
    success_url = reverse_lazy('post_list')


class PostDelete(DeleteView):
    model = Post
    template_name = 'delete.html'
    success_url = reverse_lazy('post_list')


