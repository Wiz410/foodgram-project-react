from django.contrib.auth import get_user_model

from .models import Follow

User = get_user_model()


def get_follow(user: User, id: int) -> bool:
    """Проверка подписки на пользователя.

    Args:
        user (User): Пользователь.
        id (int): ID пользователя для подписки.

    Returns:
        bool: Подписан пользователь или нет.
    """
    if user.is_anonymous:
        return False
    return Follow.objects.filter(
        user=user,
        following=id
    ).exists()
