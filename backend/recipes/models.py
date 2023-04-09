from django.core.validators import validate_slug, MaxLengthValidator
from django.db import models


class Tag(models.Model):
    color = models.CharField(
        verbose_name='Цвет',
        max_length=7,
        validators=[MaxLengthValidator(limit_value=7)],
        blank=False,
        null= True,
        default= 0
    )
    name = models.CharField(
        verbose_name='Название тега',
        max_length=200,
        validators=[MaxLengthValidator(limit_value=200)],
        blank=False
    )
    slug = models.SlugField(
        verbose_name='Уникальная строка-идентификатор',
        max_length=200,
        validators=[validate_slug, MaxLengthValidator(limit_value=200)],
        blank=False,
        null=True,
        default=0
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['-id']


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Название ингридиента',
        max_length=200,
        validators=[MaxLengthValidator(limit_value=200)],
        blank=False
    )
    measurement_unit = models.CharField(
        verbose_name='Единицы измерения',
        max_length=200,
        validators=[MaxLengthValidator(limit_value=200)],
        blank=False
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ['-id']