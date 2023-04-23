from typing import Optional

from django.core.validators import MaxLengthValidator, validate_slug, validate_integer
from django.db import models
from django.db.models import Exists, OuterRef

from recipes.validators import validate_cooking_time
from users.models import User


class Tag(models.Model):
    color = models.CharField(
        verbose_name='Цвет',
        max_length=7,
        validators=[MaxLengthValidator(limit_value=7)],
    )
    name = models.CharField(
        verbose_name='Название тега',
        max_length=200,
        validators=[MaxLengthValidator(limit_value=200)],
    )
    slug = models.SlugField(
        verbose_name='Уникальная строка-идентификатор',
        max_length=200,
        validators=[
            validate_slug,
            MaxLengthValidator(limit_value=200)
        ],
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['-id']


class Ingredient(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единицы измерения'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name} ({self.measurement_unit})'


class RecipeQuerySet(models.QuerySet):

    def add_user_annotations(self, user_id: Optional[int]):
        return self.annotate(
            is_favorited=Exists(
                Favorite.objects.filter(
                    user_id=user_id, recipe__pk=OuterRef('pk')
                )
            ),
        )


class Recipe(models.Model):
    tags = models.ManyToManyField(
        to=Tag,
        through='RecipeTag',
        through_fields=('recipe', 'tag'),
        verbose_name='Теги'
    )
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор')
    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта')
    text = models.TextField(verbose_name='Текст')
    ingredients = models.ManyToManyField(
        to=Ingredient,
        through='RecipeIngredient',
        through_fields=('recipe', 'ingredient'),
        verbose_name='Ингредиенты')
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True
    )
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления',
        max_length=10,
        validators=[
            validate_cooking_time,
            validate_integer
        ],
        help_text='Required. 10 characters or fewer.',
    )

    objects = RecipeQuerySet.as_manager()

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    amount = models.PositiveIntegerField(
        verbose_name='Количество'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )

    def __str__(self):
        return f'{self.ingredient} в {self.recipe}'

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'


class Favorite(models.Model):
    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Подписчик',
        null=True,  # null нужен, чтобы не ругался при создании на отправку пустой формы
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт',
        null=True,  # null нужен, чтобы не ругался при создании на отправку пустой формы
    )

    def __str__(self):
        return f'Избранный {self.recipe} у {self.follower}'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('follower', 'recipe'),
                name='unique_favorite_follower_recipe'
            )
        ]
        verbose_name = 'Объект избранного'
        verbose_name_plural = 'Объекты избранного'


class RecipeTag(models.Model):
    tag = models.ForeignKey(
        to=Tag,
        on_delete=models.SET_NULL,
        verbose_name='Тег',
        null=True,
    )
    recipe = models.ForeignKey(
        to=Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Тег/Рецепт'
        verbose_name_plural = 'Теги/Рецепты'
        ordering = ('-id',)


