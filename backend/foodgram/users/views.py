from django.urls import reverse_lazy
from django.views.generic import CreateView

from backend.foodgram.users.forms import CreationForm


class SignUp(CreateView):
    """Регистрации пользователя"""
    form_class = CreationForm
    # success_url = reverse_lazy('posts:index')
    # template_name = 'users/signup.html'


class PasswordResetView(CreateView):
    """Сброс пароля"""
    form_class = CreateView
    # success_url = reverse_lazy('users:password_reset_done')
    # template_name = 'users/password_reset_form.html'


class PasswordResetDoneView(CreateView):
    form_class = CreateView
    # template_name = 'users/password_reset_done.html'


class PasswordResetConfirmView(CreateView):
    form_class = CreateView
    # success_url = reverse_lazy('users:password_reset_complete')
    # template_name = 'users/password_reset_confirm.html'


class PasswordResetCompleteView(CreateView):
    form_class = CreateView
    # template_name = 'users/password_reset_complete.html'
