from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from mailing.views import OwnerRequiredMixin, ManagerOrOwnerRequiredMixin
from message.models import Message
from django.urls import reverse_lazy
from message.forms import MessageForm


class MessageCreateView(LoginRequiredMixin, CreateView):
    """Контроллер создания сообщения для рассылки"""
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('message:message_list')

    def form_valid(self, form):  # автоматическое присвоение автора
        if form.is_valid():
            product = form.save()
            product.created_by = self.request.user
            product.save()

        return super().form_valid(form)


class MessageListView(ListView):
    """Контроллер просмотра списка сообщений для рассылки"""
    model = Message
    paginate_by = 6  # количество элементов на одну страницу
    ordering = ['-id']

    def dispatch(self, request, *args, **kwargs):  # запрет доступа без авторизации
        if self.request.user.is_anonymous:
            return redirect('mailing:access_error')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self, *args, **kwargs):  # # отображение только тех сообщений, которые созданы пользователем
        queryset = super().get_queryset()
        if not self.request.user.is_manager:  # менеджеру доступны все сообщения
            queryset = queryset.filter(created_by=self.request.user.pk)
        return queryset


class MessageDetailView(ManagerOrOwnerRequiredMixin, DetailView):
    """Контроллер просмотра отдельного сообщения для рассылки"""
    model = Message


class MessageUpdateView(OwnerRequiredMixin, UpdateView):
    """Контроллер редактирования сообщения для рассылки"""
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('message:message_list')


class MessageDeleteView(OwnerRequiredMixin, DeleteView):
    """Контроллер удаления сообщения для рассылки"""
    model = Message
    success_url = reverse_lazy('message:message_list')
