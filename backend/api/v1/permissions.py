from rest_framework import permissions
from rest_framework.request import Request


class AuthorOrReadOnly(permissions.BasePermission):
    """Разрешение для авторов или чтение."""
    def has_permission(
        self,
        request: Request,
        view: any
    ) -> bool:
        """Разрешения на уровне запроса.

        Args:
            - request (Request): Запрос.
            - view (any): Метод или класс обработки запроса.
        Returns:
            - bool: Доступ если запрос безопасный
            или пользователь авторизованный.
        """
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(
        self,
        request: Request,
        view: any,
        obj: any
    ) -> bool:
        """Разрешения на уровне объекта.

        Args:
            - request (Request): Запрос.
            - view (any): Метод или класс обработки запроса.
            - obj (any): Объект.

        Returns:
            - bool: Доступ если запрос безопасный
            или пользователь авторизованный и автор объекта.
        """

        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and obj.author == request.user
        )
