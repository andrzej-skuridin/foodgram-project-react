# Generated by Django 3.2.3 on 2023-04-23 09:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0003_recipe_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShoppingCart',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'client',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name='Покупатель',
                    ),
                ),
                (
                    'recipe',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='recipes.recipe',
                        verbose_name='Рецепт',
                    ),
                ),
            ],
            options={
                'verbose_name': 'Покупка',
                'verbose_name_plural': 'Покупки',
            },
        ),
    ]
