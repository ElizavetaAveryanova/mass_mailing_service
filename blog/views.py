from django.views.generic import ListView, DetailView
from blog.models import Article

from django.shortcuts import render
# from django.urls import reverse_lazy

# from mailing.models import Mailing


def main(request):
    from client.models import Client
    # client = len(Client.objects.all().distinct('email'))
    blog = Article.objects.filter(is_published=True).order_by('?')
    # mailing = len(Mailing.objects.all())
    # mailing_active = len(Mailing.objects.filter(status=2))
    context = {
        'blog': blog[:3],
        # 'mailing': mailing,
        # 'mailing_active': mailing_active,
        # 'client': client
    }
    return render(request, 'mailing/base.html', context)
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

# class ArticleDelete(DeleteView):
#     """Контроллер удаления отдельной статьи"""
#     Model = Article
#     success_url = reverse_lazy('blog:article_list')
#
# class ArticleUpdateView(UpdateView):
#     """Контроллер изменения отдельной статьи"""
#     model = Article
#     fields = ('title', 'body', 'preview',)
#     success_url = reverse_lazy('blog:')