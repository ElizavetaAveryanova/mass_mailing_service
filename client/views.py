from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from client.models import Client
from django.urls import reverse_lazy
from client.forms import ClientForm
from mailing.views import OwnerRequiredMixin, ManagerOrOwnerRequiredMixin


class ClientCreateView(LoginRequiredMixin, CreateView):
    """Контроллер создания клиента сервиса"""
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('client:client_list')

    def form_valid(self, form):  # автоматическое присвоение автора
        if form.is_valid():
            contact = form.save()
            contact.created_by = self.request.user
            contact.save()

        return super().form_valid(form)


class ClientListView(ListView):
    """Контроллер просмотра списка клиентов сервиса"""
    model = Client
    paginate_by = 15  # количество элементов на одну страницу
    ordering = ['-id']

    def dispatch(self, request, *args, **kwargs):  # запрет доступа без авторизации
        if self.request.user.is_anonymous:
            return redirect('mailing:access_error')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self, *args, **kwargs):  # отображение только тех контактов, которые созданы пользователем
        queryset = super().get_queryset()
        if not self.request.user.is_manager:  # менеджеру доступны все контакты
            queryset = queryset.filter(created_by=self.request.user.pk)
        return queryset


class ClientDetailView(ManagerOrOwnerRequiredMixin, DetailView):
    """Контроллер просмотра отдельного клиента сервиса"""
    model = Client


class ClientUpdateView(OwnerRequiredMixin, UpdateView):
    """Контроллер редактирования клиента сервиса"""
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('client:client_list')


class ClientDeleteView(OwnerRequiredMixin, DeleteView):
    """Контроллер удаления клиента сервиса"""
    model = Client
    success_url = reverse_lazy('client:client_list')
