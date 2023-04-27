from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxLengthValidator, validate_email
from django.db import models


class User(AbstractUser):
    # Эти 2 константы нужны, чтобы получать токен по полю email вместо username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'first_name',
        'last_name',
        'password',
        'username',
    ]
    email = models.EmailField(
        max_length=254,
        unique=True,
        blank=False,
        validators=[validate_email, MaxLengthValidator(limit_value=254)],
        help_text='Required. 254 characters or fewer.',
    )
    first_name = models.CharField(
        max_length=150,
        blank=False,
        validators=[MaxLengthValidator(limit_value=150)],
        help_text='Required. 150 characters or fewer.',
    )
    last_name = models.CharField(
        max_length=150,
        blank=False,
        validators=[MaxLengthValidator(limit_value=150)],
        help_text='Required. 150 characters or fewer.',
    )
    password = models.CharField(
        max_length=150,
        blank=False,
        validators=[MaxLengthValidator(limit_value=150)],
        help_text='Required. 150 characters or fewer.',
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-username']


class Subscription(models.Model):
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='in_subscriptions',
    )

    follower = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        verbose_name='Подписчик',
        related_name='subscriptions',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
