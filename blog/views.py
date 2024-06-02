from django.views.generic import ListView, DetailView
from blog.models import Article

from django.shortcuts import render


# def main(request):
#     blog = Article.objects.filter(is_published=True).order_by('?')
#
#     context = {
#         'blog': blog[:3],
#
#     }
#     return render(request, 'mailing/base.html', context)
class ArticleListView(ListView):
    """Контроллер просмотра списка статей"""
    model = Article
    paginate_by = 6  # количество элементов на одну страницу


class ArticleDetailView(DetailView):
    """Контроллер просмотра отдельной статьи"""
    model = Article

    def get_object(self, queryset=None):  # счетчик просмотров
        article = super().get_object(queryset)
        article.views_count += 1
        article.save()
        return article
