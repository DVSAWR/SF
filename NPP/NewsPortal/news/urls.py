from django.urls import path
from .views import upgrade_me, subscribe, unsubscribe
from .views import NewsList, NewsDetail,NewsSearch,NewsUpdate,NewsCreate,NewsDelete,ArticleCreate,ArticleDelete,ArticleUpdate,CategoryListView
urlpatterns = [
    path('', NewsList.as_view(),name='post_list'),
    path('<int:pk>', NewsDetail.as_view(),name='post_detail'),
    path('search/',NewsSearch.as_view(),name='post_search'),
    path('news/<int:pk>/edit/', NewsUpdate.as_view(),name='news_edit'),
    path('news/create/',NewsCreate.as_view(),name='news_create'),
    path('news/<int:pk>/delete/',NewsDelete.as_view(),name='news_delete'),
    path('article/<int:pk>/edit/', ArticleUpdate.as_view(), name='news_edit'),
    path('article/create/', ArticleCreate.as_view(), name='news_create'),
    path('article/<int:pk>/delete/', ArticleDelete.as_view(), name='news_delete'),
    path('upgrade/', upgrade_me, name = 'upgrade'),
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/subscribe/', subscribe, name='subscribe'),
    path('categories/<int:pk>/unsubscribe/', unsubscribe, name='unsubscribe'),

]