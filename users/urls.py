from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from users.apps import UsersConfig
from users.views import RegisterView, ProfileView, verify, check_email, PasswordResetView
from users.views import UserListView, UserUpdateView

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('verify/<int:id_user>', verify, name='verify'),
    path('check_email', check_email, name='check_email'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('list/', UserListView.as_view(), name='user_list'),
    path('edit/<int:pk>/', UserUpdateView.as_view(), name='user_edit'),
]