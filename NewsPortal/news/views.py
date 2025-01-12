from django.shortcuts import render

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .filters import PostFilter
from .forms import PostForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin


class PostList(ListView):
    model = Post
    ordering = '-date_in'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

class PostSearch(ListView):
    model = Post
    ordering = '-date_in'
    template_name = 'search.html'
    context_object_name = 'search'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filterset"] = self.filterset
        return context

class NewsCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post')
    model = Post
    form_class = PostForm
    template_name = 'news_create.html'

class ArticleCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post')
    model = Post
    form_class = PostForm
    template_name = 'article_create.html'

class NewsUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post')
    model = Post
    form_class = PostForm
    template_name = 'news_create.html'

class ArticleUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post')
    model = Post
    form_class = PostForm
    template_name = 'article_create.html'

class NewsDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('post_list')

class ArticleDelete(DeleteView):
    model = Post
    template_name = 'article_delete.html'
    success_url = reverse_lazy('post_list')