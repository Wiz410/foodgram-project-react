from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from api.v1.paginations import RecipeAndSubscriptionPagination
from users.models import Follow

from .serializers import FollowSerializer

User = get_user_model()


class FoodgramUsersViewSet(UserViewSet):
    """Обработка запросов `users` с помощью `djoser`.
    Запросы к `api/users/` доступны любому пользователю.
    """
    pagination_class = LimitOffsetPagination
    permission_classes = [AllowAny]
    search_fields = ('username',)

    @action(
        methods=['get'],
        permission_classes=[IsAuthenticated],
        detail=False,
    )
    def me(self, request, *args, **kwargs):
        return super().me(request, *args, **kwargs)

    @action(
        methods=['get'],
        detail=False,
        permission_classes=[IsAuthenticated],
        pagination_class=LimitOffsetPagination,
    )
    def subscriptions(self, request):
        """Обработка запросов `subscriptions`.
        Запросы к `api/users/subscriptions/`
        доступны авторизированому пользователю.
        """
        author = Follow.objects.filter(user=request.user)
        paginator = RecipeAndSubscriptionPagination()
        result = paginator.paginate_queryset(author, request)
        serializer = FollowSerializer(
            result,
            many=True,
            context={'request': request}
        )
        return paginator.get_paginated_response(serializer.data)

    @action(
        methods=['post', 'delete'],
        detail=True,
        permission_classes=[IsAuthenticated],
    )
    def subscribe(self, request, id=None):
        """Обработка запросов `subscribe`.
        Запросы к `api/users/id/subscribe/`
        доступны авторизированому пользователю.
        """
        author = get_object_or_404(User, id=id)
        follow = Follow.objects.filter(user=request.user, author=author)
        if request.method == 'POST':
            if request.user == author:
                return Response(
                    {'error': 'Нельзя подписаться на самого себя.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if follow.exists():
                return Response(
                    {'error': f'Вы уже подписаны на {author}.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            follow = Follow.objects.create(user=request.user, author=author)
            serializer = FollowSerializer(follow, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            if follow.exists():
                follow.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(
                {'error': f'Вы не были подписаны на {author}.'},
                status=status.HTTP_400_BAD_REQUEST
            )
