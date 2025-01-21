from django.urls import path
# Импортируем созданное нами представление
from .views import (PostList, PostDetail, PostSearch, NewsCreateView, ArticleCreateView, NewsUpdateView, ArticleUpdateView, NewsDelete,
                    ArticleDelete, CategoryListView, subscribe)


urlpatterns = [
   path('news/', PostList.as_view(), name='post_list'),
   path('news/<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('news/search', PostSearch.as_view()),
   path('news/create', NewsCreateView.as_view(), name='news_create'),
   path('articles/create', ArticleCreateView.as_view(), name='article_create'),
   path('news/<int:pk>/edit', NewsUpdateView.as_view(), name='news_update'),
   path('articles/<int:pk>/edit', ArticleUpdateView.as_view(), name='article_update'),
   path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
   path('articles/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
   path('categories/<int:pk>/', CategoryListView.as_view(), name="category_list"),
   path('categories/<int:pk>/subscribe/', subscribe, name='subscribe')
]
