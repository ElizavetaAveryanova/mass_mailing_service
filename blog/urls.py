from django.urls import path
from django.views.decorators.cache import cache_page
from blog.views import ArticleListView, ArticleDetailView
from blog.apps import BlogConfig

app_name = BlogConfig.name

urlpatterns = [
    path('list/', cache_page(60)(ArticleListView.as_view()), name='article_list'),
    path('article_view/<int:pk>/', cache_page(60)(ArticleDetailView.as_view()), name='article_detail'),
]