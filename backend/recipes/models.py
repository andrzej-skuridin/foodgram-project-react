from django.core.validators import validate_slug, MaxLengthValidator, validate_integer
from django.db import models

from recipes.validators import validate_cooking_time
from users.models import User


class Tag(models.Model):
    color = models.CharField(
        verbose_name='Цвет',
        max_length=7,
        validators=[MaxLengthValidator(limit_value=7)],
        blank=False,
        null=True,
        default=0
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
        blank=False,
        help_text='Required. 200 characters or fewer.'
    )
    measurement_unit = models.CharField(
        verbose_name='Единицы измерения',
        max_length=200,
        validators=[MaxLengthValidator(limit_value=200)],
        blank=False,
        help_text='Required. 200 characters or fewer.'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ['-id']


class Recipe(models.Model):
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='recipes_by_this_author',
        verbose_name='Автор',
        blank=False,
        null=True,
    )
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления',
        max_length=10,
        validators=[MaxLengthValidator(limit_value=10),
                    validate_cooking_time,
                    validate_integer],
        blank=False,
        help_text='Required. 10 characters or fewer.',
        null=True
    )
    text = models.TextField(
        verbose_name='Описание',
        help_text='Required.',
        blank=False,
        null=True,
    )
    name = models.CharField(
        verbose_name='Название',
        max_length=200,
        validators=[MaxLengthValidator(limit_value=200)],
        help_text='Required. 200 characters or fewer.',
        blank=False,
        null=True,
    )
    # image = models.ImageField(
    #     verbose_name='Картинка',
    #     # upload_to='posts/',
    #     blank=False
    # )
    ingredients = models.ManyToManyField(
        to=Ingredient,
        through='IngredientRecipe',
        blank=False,
    )
    tags = models.ManyToManyField(
        to=Tag,
        through='TagRecipe',
        blank=False,
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-id']


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(
        to=Ingredient,
        db_column='ingredient_id',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    recipe = models.ForeignKey(
        to=Recipe,
        db_column='recipe_id',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Ингредиент/Рецепт'
        verbose_name_plural = 'Ингредиенты/Рецепты'
        ordering = ('-id',)


class TagRecipe(models.Model):
    tag = models.ForeignKey(
        to=Tag,
        db_column='tag_id',
        on_delete=models.SET_NULL,
        blank=False,
        null=True,
    )
    recipe = models.ForeignKey(
        to=Recipe,
        db_column='recipe_id',
        on_delete=models.SET_NULL,
        blank=False,
        null=True,
    )

    class Meta:
        verbose_name = 'Тег/Рецепт'
        verbose_name_plural = 'Теги/Рецепты'
        ordering = ('-id',)
