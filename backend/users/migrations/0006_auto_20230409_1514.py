# Generated by Django 3.2.3 on 2023-04-09 12:14

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_user_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(help_text='Required. 254 characters or fewer.', max_length=254, unique=True, validators=[django.core.validators.EmailValidator(), django.core.validators.MaxLengthValidator(limit_value=254)]),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(help_text='Required. 150 characters or fewer.', max_length=150, validators=[django.core.validators.MaxLengthValidator(limit_value=150)]),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(help_text='Required. 150 characters or fewer.', max_length=150, validators=[django.core.validators.MaxLengthValidator(limit_value=150)]),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(help_text='Required. 150 characters or fewer.', max_length=150, validators=[django.core.validators.MaxLengthValidator(limit_value=150)]),
        ),
    ]