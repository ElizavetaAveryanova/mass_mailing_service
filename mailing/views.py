from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView, DeleteView

from client.models import Client
from mailing.models import Mailing, Log
from django.urls import reverse_lazy


class IndexView(TemplateView):
    """Контроллер просмотра домашней страницы"""
    template_name = 'mailing/index.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['mailing_count'] = Mailing.objects.all().count()  # количество рассылок всего
        context_data['mailing_started_count'] = Mailing.objects.filter(status='STARTED').count()  # активных рассылок
        context_data['mailing_clients_count'] = Client.objects.all().count()  # уникальных клиентов

        return context_data


class MailingCreateView(CreateView):
    """Контроллер создания рассылки"""
    model = Mailing
    success_url = reverse_lazy('mailing:mailing_list')


class MailingListView(ListView):
    """Контроллер просмотра списка рассылок"""
    model = Mailing
    paginate_by = 9  # количество элементов на одну страницу


class MailingDetailView(DetailView):
    """Контроллер просмотра отдельной рассылки"""
    model = Mailing


class MailingUpdateView(UpdateView):
    """Контроллер редактирования рассылки"""
    model = Mailing
    success_url = reverse_lazy('mailing:mailing_list')


class MailingDeleteView(DeleteView):
    """Контроллер удаления рассылки"""
    model = Mailing
    success_url = reverse_lazy('mailing:mailing_list')


class LogListView(ListView):
    """Контроллер просмотра логов"""
    model = Log
    paginate_by = 9  # количество элементов на одну страницу



class LogDetailView(DetailView):
    """Контроллер просмотра отдельного лога"""
    model = Log

