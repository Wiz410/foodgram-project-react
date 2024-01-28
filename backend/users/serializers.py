from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from api.v1.tools import ShortRecipeSerialize
from recipes.models import Recipe

from .models import Follow
from .tools import get_follow

USER = get_user_model()
GET_USER = USER.objects.all()
MAX_LENGTH_EMAIL: int = 254
MAX_LENGTH_USERNAME: int = 150


class FoodgramUserCreateSerializer(UserCreateSerializer):
    """Сериализатор регистрации пользователя для `Djoser`."""
    email = serializers.EmailField(
        max_length=MAX_LENGTH_EMAIL,
        validators=[
            UniqueValidator(
                GET_USER,
                (
                    'Пользователь с таким адресом электронной почты '
                    'уже существует.'
                )
            ),
        ]
    )
    username = serializers.CharField(
        max_length=MAX_LENGTH_USERNAME,
        validators=[
            UniqueValidator(
                GET_USER,
                'Пользователь с таким именем аккаунта уже существует.'
            ),
            RegexValidator(
                r'^[\w.@+-]+\Z',
                'Имя аккаунта указан не корректно',
            ),
        ]
    )

    class Meta:
        model = USER
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
        model = USER
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj: USER) -> bool:
        """Проверка подписки на пользователя.

        Args:
            - obj (USER): Модель пользователя.

        Returns:
            - bool: Подписан пользователь или нет.
        """
        return get_follow(self.context['request'].user, obj.id)


class FollowSerializer(serializers.ModelSerializer):
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
            - obj (USER): Модель пользователя.

        Returns:
            - bool: Подписан пользователь или нет.
        """
        return get_follow(self.context['request'].user, obj.following)

    def get_recipes(self, obj):
        limit = self.context.get(
            'request'
        ).query_params.get('recipes_limit')
        recipe = Recipe.objects.filter(author=obj.following)
        if limit:
            recipe = recipe[:int(limit)]
        return ShortRecipeSerialize(recipe, many=True).data

    def get_recipes_count(self, obj):
        return obj.following.recipe_author.count()
