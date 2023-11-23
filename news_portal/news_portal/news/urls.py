from django.urls import path

from .views import PostList, PostDetail, PostSearch, PostCreate, PostUpdate, PostDelete, UserDetail, UserUpdate, join_author_group, CategoryListView, subscribe, unsubscribe


urlpatterns = [
    path('', PostList.as_view(), name='news_list'),
    path('<int:pk>', PostDetail.as_view(), name='news_detail'),
    path('search/', PostSearch.as_view(), name='news_search'),
    path('create/', PostCreate.as_view(), name='news_create'),
    path('<int:pk>/edit', PostUpdate.as_view(), name='news_edit'),
    path('<int:pk>/delete', PostDelete.as_view(), name='news_delete'),
    path('article/create/', PostCreate.as_view(), name='article_create'),
    path('article/<int:pk>/edit', PostUpdate.as_view, name='article_edit'),
    path('article/<int:pk>/delete', PostDelete.as_view(), name='article_delete'),
    path('user/<int:pk>', UserDetail.as_view(), name='user_detail'),
    path('user/<int:pk>/edit', UserUpdate.as_view(), name='user_edit'),
    path('join/', join_author_group, name='join_author_group'),
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/subscribe/', subscribe, name='subscribe'),
    path('categories/<int:pk>/unsubscribe/', unsubscribe, name='unsubscribe'),

]

