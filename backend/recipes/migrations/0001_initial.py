# Generated by Django 3.2.3 on 2023-04-09 08:53

import django.core.validators
from django.db import migrations, models
import re


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(max_length=7, validators=[django.core.validators.MaxLengthValidator(limit_value=7)], verbose_name='Цвет')),
                ('name', models.CharField(max_length=200, validators=[django.core.validators.MaxLengthValidator(limit_value=200)], verbose_name='Название тега')),
                ('slug', models.SlugField(max_length=200, validators=[django.core.validators.RegexValidator(re.compile('^[-a-zA-Z0-9_]+\\Z'), 'Enter a valid “slug” consisting of letters, numbers, underscores or hyphens.', 'invalid'), django.core.validators.MaxLengthValidator(limit_value=200)], verbose_name='Уникальная строка-идентификатор')),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
                'ordering': ['-id'],
            },
        ),
    ]
