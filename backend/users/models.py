from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import UniqueConstraint

MAX_LENGTH_EMAIL: int = 254
MAX_LENGTH_FIELD: int = 150
HELP_MESSAGE_REQUIRED: str = 'Обязательно для заполнения, '
HELP_MESSAGE_MAX: str = 'не более 150 символов.'


class FoodgramUser(AbstractUser):
    """Модель пользователя `Foodgram`."""
    email = models.EmailField(
        'Электронная почта',
        max_length=MAX_LENGTH_EMAIL,
        unique=True,
        help_text=(
            f'{HELP_MESSAGE_REQUIRED} не более 254 символов.'
        ),
    )
    username = models.CharField(
        'Имя аккаунта',
        max_length=MAX_LENGTH_FIELD,
        unique=True,
        help_text=f'{HELP_MESSAGE_REQUIRED}{HELP_MESSAGE_MAX}',
        validators=[
            RegexValidator(
                r'^[\w.@+-]+\Z',
                'Имя аккаунта указан не корректно',
            ),
        ]
    )
    first_name = models.CharField(
        'Имя',
        max_length=MAX_LENGTH_FIELD,
        help_text=f'{HELP_MESSAGE_REQUIRED}{HELP_MESSAGE_MAX}',
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=MAX_LENGTH_FIELD,
        help_text=f'{HELP_MESSAGE_REQUIRED}{HELP_MESSAGE_MAX}',
    )
    password = models.CharField(
        'Пароль',
        max_length=MAX_LENGTH_FIELD,
        help_text=f'{HELP_MESSAGE_REQUIRED}{HELP_MESSAGE_MAX}',
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
        verbose_name='Пользователь',
        help_text='Пользователь который подписан.',
    )
    following = models.ForeignKey(
        FoodgramUser,
        on_delete=models.CASCADE,
        related_name='follow_following',
        verbose_name='Подписан на пользователя',
        help_text='Пользователь на которого подписаны.',
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
