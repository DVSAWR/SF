from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from rest_framework.authentication import SessionAuthentication

from .models import Post, Author, Category, User
from .filters import PostFilter, FilterSet
from .forms import PostForm, AuthorForm, UserForm


class PostList(ListView):
    model = Post
    ordering = '-post_create_datetime'
    template_name = 'news_list.html'
    context_object_name = 'news_list'
    paginate_by = 3


class PostDetail(DetailView):
    model = Post
    template_name = 'news_detail.html'
    context_object_name = 'news_detail'


class PostSearch(ListView):
    model = Post
    template_name = 'news_search.html'
    context_object_name = 'news_search'
    ordering = ['-post_create_datetime']
    paginate_by = 3

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'news_create.html'
    context_object_name = 'news_create'

    def form_valid(self, form):
        post = form.save(commit=False)
        if 'article' in self.request.path:
            post.post_type = 'ARL'
        elif 'news/create/' in self.request.path:
            post.post_type = 'NWS'
        post.save()
        return super().form_valid(form)


class PostUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('news.create_post',)
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'


class PostDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')


class UserDetail(DetailView):
    model = User
    template_name = 'user_detail.html'
    context_object_name = 'user_detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_premium'] = not self.request.user.groups.filter(name='premium').exists()
        return context


class UserUpdate(LoginRequiredMixin, UpdateView):
    form_class = UserForm
    model = User
    template_name = 'user_edit.html'
    context_object_name = 'user_edit'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_premium'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class CategoryListView(ListView):
    model = Category
    template_name = 'category_news_list.html'
    context_object_name = 'category_news_list'
    paginate_by = 10


@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(pk=pk)
    category.subscribers.add(user)
    return redirect('category_list')


@login_required
def unsubscribe(request, pk):
    user = request.user
    category = Category.objects.get(pk=pk)
    category.subscribers.remove(user)
    return redirect('/news/categories')


@login_required
def join_author_group(request):
    user = request.user
    author_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        author_group.user_set.add(user)
    return redirect('/news/categories')





