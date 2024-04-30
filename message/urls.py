from django.urls import path
from message.views import MessageListView, MessageCreateView
from message.views import MessageDetailView, MessageUpdateView, MessageDeleteView
from message.apps import MessageConfig

app_name = MessageConfig.name

urlpatterns = [
    path('list/', MessageListView.as_view(), name='message_list'),
    path('create/', MessageCreateView.as_view(), name='message_create'),
    path('view/<int:pk>/', MessageDetailView.as_view(), name='message_detail'),
    path('edit/<int:pk>/', MessageUpdateView.as_view(), name='message_edit'),
    path('delete/<int:pk>/', MessageDeleteView.as_view(), name='message_delete'),
]
