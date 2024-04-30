from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from message.models import Message
from django.urls import reverse_lazy



class MessageCreateView(CreateView):
    """Контроллер создания сообщения для рассылки"""
    model = Message
    success_url = reverse_lazy('message:message_list')


class MessageListView(ListView):
    """Контроллер просмотра списка сообщений для рассылки"""
    model = Message
    paginate_by = 6  # количество элементов на одну страницу


class MessageDetailView(DetailView):
    """Контроллер просмотра отдельного сообщения для рассылки"""
    model = Message


class MessageUpdateView(UpdateView):
    """Контроллер редактирования сообщения для рассылки"""
    model = Message
    success_url = reverse_lazy('message:message_list')


class MessageDeleteView(DeleteView):
    """Контроллер удаления сообщения для рассылки"""
    model = Message
    success_url = reverse_lazy('message:message_list')
