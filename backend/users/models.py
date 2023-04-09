from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxLengthValidator, validate_email
from django.db import models


class User(AbstractUser):
    email = models.EmailField(
        max_length=254,
        unique=True,
        blank=False,
        validators=[validate_email, MaxLengthValidator(limit_value=254)],
        help_text='Required. 254 characters or fewer.'
    )
    first_name = models.CharField(
        max_length=150,
        blank=False,
        validators=[MaxLengthValidator(limit_value=150)],
        help_text='Required. 150 characters or fewer.'
    )
    last_name = models.CharField(
        max_length=150,
        blank=False,
        validators=[MaxLengthValidator(limit_value=150)],
        help_text='Required. 150 characters or fewer.'
    )
    password = models.CharField(
        max_length=150,
        blank=False,
        validators=[MaxLengthValidator(limit_value=150)],
        help_text='Required. 150 characters or fewer.'
        )

    # is_subscribed = models.CharField(
    #     max_length=10,
    #     blank=False
    # )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-username']
