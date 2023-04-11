# Generated by Django 3.2.3 on 2023-04-11 17:46

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import re
import recipes.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Required. 200 characters or fewer.', max_length=200, validators=[django.core.validators.MaxLengthValidator(limit_value=200)], verbose_name='Название ингридиента')),
                ('measurement_unit', models.CharField(help_text='Required. 200 characters or fewer.', max_length=200, validators=[django.core.validators.MaxLengthValidator(limit_value=200)], verbose_name='Единицы измерения')),
            ],
            options={
                'verbose_name': 'Ингредиент',
                'verbose_name_plural': 'Ингредиенты',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='IngredientRecipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ingredient', models.ForeignKey(blank=True, db_column='ingredient_id', null=True, on_delete=django.db.models.deletion.SET_NULL, to='recipes.ingredient')),
            ],
            options={
                'verbose_name': 'Ингредиент/Рецепт',
                'verbose_name_plural': 'Ингредиенты/Рецепты',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cooking_time', models.IntegerField(help_text='Required. 10 characters or fewer.', max_length=10, null=True, validators=[django.core.validators.MaxLengthValidator(limit_value=10), recipes.validators.validate_cooking_time, django.core.validators.validate_integer], verbose_name='Время приготовления')),
                ('text', models.TextField(help_text='Required.', null=True, verbose_name='Описание')),
                ('name', models.CharField(help_text='Required. 200 characters or fewer.', max_length=200, null=True, validators=[django.core.validators.MaxLengthValidator(limit_value=200)], verbose_name='Название')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='recipes_by_this_author', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('ingredients', models.ManyToManyField(through='recipes.IngredientRecipe', to='recipes.Ingredient')),
            ],
            options={
                'verbose_name': 'Рецепт',
                'verbose_name_plural': 'Рецепты',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(default=0, max_length=7, null=True, validators=[django.core.validators.MaxLengthValidator(limit_value=7)], verbose_name='Цвет')),
                ('name', models.CharField(max_length=200, validators=[django.core.validators.MaxLengthValidator(limit_value=200)], verbose_name='Название тега')),
                ('slug', models.SlugField(default=0, max_length=200, null=True, validators=[django.core.validators.RegexValidator(re.compile('^[-a-zA-Z0-9_]+\\Z'), 'Enter a valid “slug” consisting of letters, numbers, underscores or hyphens.', 'invalid'), django.core.validators.MaxLengthValidator(limit_value=200)], verbose_name='Уникальная строка-идентификатор')),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='TagRecipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(db_column='recipe_id', null=True, on_delete=django.db.models.deletion.SET_NULL, to='recipes.recipe')),
                ('tag', models.ForeignKey(db_column='tag_id', null=True, on_delete=django.db.models.deletion.SET_NULL, to='recipes.tag')),
            ],
            options={
                'verbose_name': 'Тег/Рецепт',
                'verbose_name_plural': 'Теги/Рецепты',
                'ordering': ('-id',),
            },
        ),
        migrations.AddField(
            model_name='recipe',
            name='tag',
            field=models.ManyToManyField(through='recipes.TagRecipe', to='recipes.Tag'),
        ),
        migrations.AddField(
            model_name='ingredientrecipe',
            name='recipe',
            field=models.ForeignKey(blank=True, db_column='recipe_id', null=True, on_delete=django.db.models.deletion.SET_NULL, to='recipes.recipe'),
        ),
    ]
