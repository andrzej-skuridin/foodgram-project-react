# Generated by Django 3.2.3 on 2023-04-09 16:34

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0005_delete_subscription'),
    ]

    operations = [
        migrations.CreateModel(
            name='IngredientRecipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
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
            ],
            options={
                'verbose_name': 'Рецепт',
                'verbose_name_plural': 'Рецепты',
                'ordering': ['-id'],
            },
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='measurement_unit',
            field=models.CharField(help_text='Required. 200 characters or fewer.', max_length=200, validators=[django.core.validators.MaxLengthValidator(limit_value=200)], verbose_name='Единицы измерения'),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='name',
            field=models.CharField(help_text='Required. 200 characters or fewer.', max_length=200, validators=[django.core.validators.MaxLengthValidator(limit_value=200)], verbose_name='Название ингридиента'),
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
            name='ingredients',
            field=models.ManyToManyField(through='recipes.IngredientRecipe', to='recipes.Ingredient'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='tag',
            field=models.ManyToManyField(through='recipes.TagRecipe', to='recipes.Tag'),
        ),
        migrations.AddField(
            model_name='ingredientrecipe',
            name='ingredient',
            field=models.ForeignKey(blank=True, db_column='ingredient_id', null=True, on_delete=django.db.models.deletion.SET_NULL, to='recipes.ingredient'),
        ),
        migrations.AddField(
            model_name='ingredientrecipe',
            name='recipe',
            field=models.ForeignKey(blank=True, db_column='recipe_id', null=True, on_delete=django.db.models.deletion.SET_NULL, to='recipes.recipe'),
        ),
    ]