from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from client.models import Client
from django.urls import reverse_lazy



class ClientCreateView(CreateView):
    """Контроллер создания клиента сервиса"""
    model = Client
    success_url = reverse_lazy('client:client_list')


class ClientListView(ListView):
    """Контроллер просмотра списка клиентов сервиса"""
    model = Client
    paginate_by = 15  # количество элементов на одну страницу


class ClientDetailView(DetailView):
    """Контроллер просмотра отдельного клиента сервиса"""
    model = Client


class ClientUpdateView(UpdateView):
    """Контроллер редактирования клиента сервиса"""
    model = Client
    success_url = reverse_lazy('client:client_list')


class ClientDeleteView(DeleteView):
    """Контроллер удаления клиента сервиса"""
    model = Client
    success_url = reverse_lazy('client:client_list')
