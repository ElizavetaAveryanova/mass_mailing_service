from django.urls import path
from client.views import ClientListView, ClientCreateView
from client.views import ClientDetailView, ClientUpdateView, ClientDeleteView
from client.apps import ClientConfig

app_name = ClientConfig.name

urlpatterns = [
    path('list/', ClientListView.as_view(), name='client_list'),
    path('create/', ClientCreateView.as_view(), name='client_create'),
    path('view/<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
    path('edit/<int:pk>/', ClientUpdateView.as_view(), name='client_edit'),
    path('delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),
]
