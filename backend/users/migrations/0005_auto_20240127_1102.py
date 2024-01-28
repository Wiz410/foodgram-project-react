# Generated by Django 3.2.16 on 2024-01-27 08:02

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20240126_2039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foodgramuser',
            name='email',
            field=models.EmailField(help_text='Обязательно для заполнения,  не более 254 символов.', max_length=254, unique=True, verbose_name='Электронная почта'),
        ),
        migrations.AlterField(
            model_name='foodgramuser',
            name='first_name',
            field=models.CharField(help_text='Обязательно для заполнения, не более 150 символов.', max_length=150, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='foodgramuser',
            name='last_name',
            field=models.CharField(help_text='Обязательно для заполнения, не более 150 символов.', max_length=150, verbose_name='Фамилия'),
        ),
        migrations.AlterField(
            model_name='foodgramuser',
            name='password',
            field=models.CharField(help_text='Обязательно для заполнения, не более 150 символов.', max_length=150, verbose_name='Пароль'),
        ),
        migrations.AlterField(
            model_name='foodgramuser',
            name='username',
            field=models.CharField(help_text='Обязательно для заполнения, не более 150 символов.', max_length=150, unique=True, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+\\Z', 'Имя аккаунта указан не корректно')], verbose_name='Имя аккаунта'),
        ),
    ]
