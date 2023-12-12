from rest_framework import permissions


class AuthorOrReadOnly(permissions.BasePermission):
    """Разрещение для авторов.

    Returns:
        `has_object_permission` (bool): True если
        запрос безопасный или авторизованный пользователь автор обьекта.
    """
    def has_permission(self, request, view):
        return (
                request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
            )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and obj.author == request.user
        )
