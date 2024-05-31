import random
import string
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, UpdateView, FormView
from config import settings
from config.settings import DEFAULT_FROM_EMAIL
from users.forms import RegisterCreationForm, UserProfileForm, PasswordResetForm
from users.models import User

class RegisterView(CreateView):
    model = User
    form_class = RegisterCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:check_email')

    def form_valid(self, form):
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.id = random.randint(0, 100)
            user.save()
            send_mail(
                'Подтвердите свой электронный адрес',
                f"Ваша учетная запись подтверждена!"
                f"Перейдите по ссылке - http://127.0.0.1:8000/users/verify/{user.id}",
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )
        return super().form_valid(form)

def verify(request, id_user):
    user = User.objects.get(id=id_user)
    if user is not None and user.id == id_user:
        user.is_active = True
        user.save()
        return HttpResponseRedirect(reverse_lazy('users:login'))

def check_email(request):
    return render(request, 'users/check_email.html')

class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('mailing:index')

    def get_object(self, queryset=None):
        return self.request.user

# class PasswordResetView(View):
#     template_name = 'users/password_reset_form.html'
#     form_class = PasswordResetForm
#     success_url = reverse_lazy('users:login')
#
#     def get(self, request):
#         form = self.form_class()
#         return render(request, self.template_name, {'form': form})
#
#     def post(self, request):
#         form = self.form_class(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data['email']
#             user = get_object_or_404(User, email=email)
#             letters = list(string.ascii_lowercase)
#             new_password = ''
#             for _ in range(5):
#                 new_password = new_password + random.choice(letters) + str(random.randint(1, 9))
#             user.set_password(new_password)
#             user.save()
#             message = f"Ваш новый пароль: {new_password}\nНикому его не сообщайте."
#             send_mail(
#                 'Новый пароль',
#                 message,
#                 settings.EMAIL_HOST_USER,
#                 [user.email],
#                 fail_silently=False,
#             )
#             return redirect(self.success_url)
#         return render(request, self.template_name, {'form': form})


class PasswordResetView(FormView):
    model = User
    template_name = "users/password_reset_form.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        email_form = form.cleaned_data("email")
        user = User.objects.get(email=email_form)

        letters = list(string.ascii_lowercase)
        new_password = ''
        for _ in range(5):
            new_password = new_password + random.choice(letters) + str(random.randint(1, 9))

        user.set_password(new_password)
        user.save()
        send_mail(
            subject="Новый пароль",
            message=f"Ваш пароль: {new_password}",
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )
        return super().form_valid(form)