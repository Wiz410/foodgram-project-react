from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from api.v1.tools import ShortRecipeSerialize
from recipes.models import Recipe
from . import constants as con
from .models import Follow
from .tools import get_follow

User = get_user_model()
Get_user = User.objects.all()


class FoodgramUserCreateSerializer(UserCreateSerializer):
    """Сериализатор регистрации пользователя для `Djoser`."""
    email = serializers.EmailField(
        max_length=con.MODEL_MAX_LENGTH_EMAIL,
        validators=[
            UniqueValidator(
                Get_user,
                con.SERIALIZER_ERROR_VALIDATE_UNIQUE_EMAIL,
            ),
        ]
    )
    username = serializers.CharField(
        max_length=con.MODEL_MAX_LENGTH_FIELD,
        validators=[
            UniqueValidator(
                Get_user,
                con.SERIALIZER_ERROR_VALIDATE_UNIQUE_USERNAME,
            ),
            RegexValidator(
                r'^[\w.@+-]+\Z',
                con.MODEL_ERROR_VALIDATE_USERNAME,
            ),
        ]
    )

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
        )


class FoodgramUserSerializer(UserSerializer):
    """Сериализатор пользователей для `Djoser`."""
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj: User) -> bool:
        """Проверка подписки на пользователя.

        Args:
            - obj (User): Модель пользователя.

        Returns:
            - bool: Подписан пользователь или нет.
        """
        return get_follow(self.context['request'].user, obj.id)


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор подписок пользователей."""
    email = serializers.EmailField(
        source='following.email',
        read_only=True
    )
    id = serializers.IntegerField(
        source='following.id',
        read_only=True
    )
    username = serializers.CharField(
        source='following.username',
        read_only=True
    )
    first_name = serializers.CharField(
        source='following.first_name',
        read_only=True
    )
    last_name = serializers.CharField(
        source='following.last_name',
        read_only=True
    )
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )

    def get_is_subscribed(self, obj: Follow) -> bool:
        """Проверка подписки на пользователя.

        Args:
            - obj (Follow): Модель подписок.

        Returns:
            - bool: Подписан пользователь или нет.
        """
        return get_follow(self.context['request'].user, obj.following)

    def get_recipes(self, obj: Follow) -> ShortRecipeSerialize:
        """Получение ограниченного количества рецептов автора.

        Args:
            obj (Follow): Модель подписок.

        Returns:
            ShortRecipeSerialize: Ограниченного количества рецептов автора.
        """
        limit = self.context.get(
            'request'
        ).query_params.get('recipes_limit')
        recipe = Recipe.objects.filter(author=obj.following)
        if limit:
            recipe = recipe[:int(limit)]
        return ShortRecipeSerialize(recipe, many=True).data

    def get_recipes_count(self, obj: Follow) -> int:
        """Количество рецептов.


        Args:
            obj (Follow): Модель подписок.

        Returns:
            int: Количество рецептов у автора.
        """
        return obj.following.recipe_author.count()
