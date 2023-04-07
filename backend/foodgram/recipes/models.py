from django.core.validators import validate_slug, MaxLengthValidator, validate_integer
from django.db import models
from django.db.models import CheckConstraint, Q, F

from backend.foodgram.recipes.validators import validate_cooking_time
from backend.foodgram.users.models import User


class Tag(models.Model):
    color = models.CharField(
        verbose_name='Цвет',
        max_length=7,
        validators=[MaxLengthValidator(limit_value=7)]
    )
    name = models.CharField(
        verbose_name='Название тега',
        max_length=200,
        validators=[MaxLengthValidator(limit_value=200)]
    )
    slug = models.SlugField(
        verbose_name='Уникальная строка-идентификатор',
        max_length=200,
        validators=[validate_slug, MaxLengthValidator(limit_value=200)]
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Название ингридиента',
        max_length=200,
        validators=[MaxLengthValidator(limit_value=200)]
    )
    # amount = models.FloatField(
    #     verbose_name='Количество'
    # )
    measurement_unit = models.CharField(
        verbose_name='Единицы измерения',
        max_length=200,
        validators=[MaxLengthValidator(limit_value=200)]
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes_by_this_author',
        verbose_name='Автор'
    ),
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления',
        max_length=10,
        validators=[MaxLengthValidator(limit_value=10),
                    validate_cooking_time,
                    validate_integer]
    ),
    text = models.TextField(
        verbose_name='Описание'
    ),
    image = models.ImageField(
        verbose_name='Картинка',
        # upload_to='posts/',
        blank=True
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe',
        blank=True
    )
    name = models.CharField(
        verbose_name='Название',
        max_length=200,
        validators=[MaxLengthValidator(limit_value=200)]
    ),
    tag = models.ManyToManyField(
        Tag,
        through='TagRecipe',
        blank=True
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(Ingredient,
                                   db_column='ingredient_id',
                                   on_delete=models.SET_NULL,
                                   blank=True,
                                   null=True,
                                   )
    recipe = models.ForeignKey(Recipe,
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
    tag = models.ForeignKey(Tag,
                            db_column='tag_id',
                            on_delete=models.SET_NULL,
                            blank=True,
                            null=True,
                            )
    recipe = models.ForeignKey(Recipe,
                               db_column='recipe_id',
                               on_delete=models.SET_NULL,
                               blank=True,
                               null=True,
                               )

    class Meta:
        verbose_name = 'Тег/Рецепт'
        verbose_name_plural = 'Теги/Рецепты'
        ordering = ('-id',)


class RecipeIngredientAmount(models.Model):
    recipe_id = models.ForeignKey(
        Recipe,
        related_name='amount_of_ingredients',
        verbose_name='Рецепт',
        on_delete=models.SET_NULL,
        unique=True,
        validators=[validate_integer]
    )
    ingredient_id = models.ForeignKey(
        Ingredient,
        related_name='used_in_recipes_with_amount',
        verbose_name='Ингредиент',
        on_delete=models.SET_NULL,
        validators=[validate_integer]
    )
    amount = models.FloatField(
        verbose_name='Количество'
    )


class Subscription(models.Model):
    subscriber = models.ForeignKey(
        User,
        related_name='subscriptions',
        verbose_name='Подписчик',
        on_delete=models.SET_NULL,
    )
    author = models.ForeignKey(
        User,
        related_name='subscribers',
        verbose_name='Автор',
        on_delete=models.SET_NULL,
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        unique_together = ['subscriber', 'author']
        constraints = [
            CheckConstraint(name='not_same', check=~Q(author=F('subscriber')))
        ]

    def __str__(self):
        return f'{self.subscriber} подписан на {self.author}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        related_name='favorites_of_this_user',
        verbose_name='Пользователь',
        on_delete=models.SET_NULL,
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='in_favorites',
        verbose_name='Рецепт',
        on_delete=models.SET_NULL  # тут не уверен
    )

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'

    def __str__(self):
        return f'{self.recipe} находится в избранном пользователя {self.user}'
