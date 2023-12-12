from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import UniqueConstraint

MAX_EMAIL_FIELDS = 254
MAX_USER_FIELDS = 150


class User(AbstractUser):
    """Модель пользователя."""
    email = models.EmailField(
        unique=True,
        max_length=MAX_EMAIL_FIELDS,
        verbose_name='Адрес электронной почты',

    )
    username = models.CharField(
        unique=True,
        max_length=MAX_USER_FIELDS,
        verbose_name='Имя пользователя',
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+\Z',
                message='Некорректный ввод'
            )
        ]
    )
    first_name = models.CharField(
        max_length=MAX_USER_FIELDS,
        verbose_name='Имя',
    )
    last_name = models.CharField(
        max_length=MAX_USER_FIELDS,
        verbose_name='Фамилия',
    )
    password = models.CharField(
        max_length=MAX_USER_FIELDS,
        verbose_name='Пароль',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username',
        'first_name',
        'last_name',
        'password',
    ]

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = (
            'first_name',
            'last_name',
            'username',
            'id',
        )

    def __str__(self):
        return self.username


class Follow(models.Model):
    """Модель подписок пользователя."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Пользователь'

    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Подписан на'
    )

    class Meta:
        verbose_name = 'Подписки пользователя'
        verbose_name_plural = 'Подписки пользователей'
        ordering = (
            'user',
            'author',
        )
        constraints = [
            UniqueConstraint(
                fields=['user', 'author'],
                name='Subscriptions',
            )
        ]

    def __str__(self):
        return (
            f'Пользователь {self.user.username} '
            f'подписан на {self.author.username}'
        )
