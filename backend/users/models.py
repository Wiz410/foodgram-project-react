from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import UniqueConstraint

from . import constants as con


class FoodgramUser(AbstractUser):
    """Модель пользователя `Foodgram`."""
    email = models.EmailField(
        con.MODEL_NAME_EMAIL,
        max_length=con.MODEL_MAX_LENGTH_EMAIL,
        unique=True,
        help_text=(
            f'{con.MODEL_HELP_REQUIRED}'
            f'{con.MODEL_HELP_MAX_EMAIL}'
        ),
    )
    username = models.CharField(
        con.MODEL_NAME_USERNAME,
        max_length=con.MODEL_MAX_LENGTH_FIELD,
        unique=True,
        help_text=(
            f'{con.MODEL_HELP_REQUIRED}'
            f'{con.MODEL_HELP_MAX_FIELD}'
        ),
        validators=[
            RegexValidator(
                r'^[\w.@+-]+\Z',
                con.MODEL_ERROR_VALIDATE_USERNAME,
            ),
        ]
    )
    first_name = models.CharField(
        con.MODEL_NAME_FIRST_NAME,
        max_length=con.MODEL_MAX_LENGTH_FIELD,
        help_text=(
            f'{con.MODEL_HELP_REQUIRED}'
            f'{con.MODEL_HELP_MAX_FIELD}'
        ),
    )
    last_name = models.CharField(
        con.MODEL_NAME_LAST_NAME,
        max_length=con.MODEL_MAX_LENGTH_FIELD,
        help_text=(
            f'{con.MODEL_HELP_REQUIRED}'
            f'{con.MODEL_HELP_MAX_FIELD}'
        ),
    )
    password = models.CharField(
        con.MODEL_NAME_PASSWORD,
        max_length=con.MODEL_MAX_LENGTH_FIELD,
        help_text=(
            f'{con.MODEL_HELP_REQUIRED}'
            f'{con.MODEL_HELP_MAX_FIELD}'
        ),
    )

    USERNAME_FIELD: str = 'email'
    REQUIRED_FIELDS: list[str] = [
        'username',
        'first_name',
        'last_name',
        'password',
    ]

    class Meta:
        verbose_name: str = 'Пользователь'
        verbose_name_plural: str = 'Пользователи'
        ordering = (
            'username',
            'id',
            'email',
            'date_joined',
        )

    def __str__(self) -> str:
        return self.username


class Follow(models.Model):
    """Модель подписки пользователей."""
    user = models.ForeignKey(
        FoodgramUser,
        on_delete=models.CASCADE,
        related_name='follow_user',
        verbose_name=con.MODEL_NAME_USER,
        help_text=con.MODEL_HELP_USER,
    )
    following = models.ForeignKey(
        FoodgramUser,
        on_delete=models.CASCADE,
        related_name='follow_following',
        verbose_name=con.MODEL_NAME_FOLLOWING,
        help_text=con.MODEL_HELP_FOLLOWING,
    )

    class Meta:
        verbose_name: str = 'Подписки пользователя'
        verbose_name_plural: str = 'Подписки пользователей'
        constraints = [
            UniqueConstraint(
                fields=['user', 'following'],
                name='unique_follow'
            )
        ]
        ordering = (
            'user',
            'id',
            'following',
        )

    def __str__(self) -> str:
        return f'{self.user.username} подписан на {self.following.username}'
