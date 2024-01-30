from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from api.v1.paginations import RecipeAndSubscriptionPagination
from users.models import Follow

from .serializers import FollowSerializer

User = get_user_model()


class FoodgramUserViewSet(UserViewSet):
    """Обработка запросов к `api/users/` с `Djoser`.
    - Запросы `me/` доступны авторизованному пользователю.
    - Запросы `subscriptions/` доступны авторизованному пользователю.
    - Запросы `subscribe/` доступны авторизованному пользователю.
    - Запросы к остальным путям доступны любому пользователю.
    Raise:
        - Не работает просмотр пользователя для анонима ошибка в `frontend`.
    """
    pagination_class = LimitOffsetPagination
    permission_classes = [AllowAny]

    @action(
        methods=['get'],
        permission_classes=[IsAuthenticated],
        detail=False,
    )
    def me(self, request: Request, *args, **kwargs) -> Response:
        """Обработка запросов к `api/users/me` с `Djoser`.
        - Запросы доступны авторизованному пользователю.

        Args:
            - request (Request): Запрос.

        Returns:
            - Response: Профиль пользователя.
        """
        return super().me(request, *args, **kwargs)

    @action(
        methods=['get'],
        permission_classes=[IsAuthenticated],
        detail=False,
    )
    def subscriptions(self, request: Request) -> Response:
        """Обработка запросов к `api/users/subscriptions`.

        Args:
            - request (Request): Запрос.

        Returns:
            - Response: Пользователи на которых подписан текущий пользователь.
        """
        author = Follow.objects.filter(user=request.user)
        paginator = RecipeAndSubscriptionPagination()
        result = paginator.paginate_queryset(author, request)
        serializer = FollowSerializer(
            result,
            many=True,
            context={'request': request},
        )
        return paginator.get_paginated_response(serializer.data)

    @action(
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated],
        detail=True,
    )
    def subscribe(self, request: Request, id: int = None) -> Response:
        """Обработка запросов к `api/users/subscriptions`.

        Args:
            - request (Request): Запрос.
            - id (int): ID пользователя.

        Returns:
            - Response: Подписка `post` или отписка `delete` на пользователя.
        """
        author = get_object_or_404(User, id=id)
        follow = Follow.objects.filter(user=request.user, following=author)
        if request.method == 'POST':
            if request.user == author:
                return Response(
                    {'errors': 'Нельзя подписаться на себя'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            elif follow.exists():
                return Response(
                    {'error': 'Вы уже подписаны на пользователя'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            follow = Follow.objects.create(user=request.user, following=author)
            serializer = FollowSerializer(follow, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            if follow.exists():
                follow.delete()
                return Response(
                    status=status.HTTP_204_NO_CONTENT
                )
            return Response(
                {'error': 'Вы не были подписаны на пользователя'},
                status=status.HTTP_400_BAD_REQUEST
            )
