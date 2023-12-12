from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from api.v1.serializers import FavoriteShopAndUserSerializer
from recipe.models import Recipe
from users.models import Follow

User = get_user_model()


class FoodgramUserCreateSerializer(UserCreateSerializer):
    """Сериализатор регистрации модели `User` для `Djoser`."""
    email = serializers.EmailField(
        required=True,
        max_length=254,
        validators=[
            UniqueValidator(
                User.objects.all(),
                'Пользователь с такой почтой уже существует.',
            )
        ]
    )
    username = serializers.CharField(
        max_length=150,
        validators=[
            UniqueValidator(
                User.objects.all(),
                'Пользователь с таким именем пользователя уже существует.',
            ),
            RegexValidator(
                regex=r'^[\w.@+-]+\Z',
                message='Некорректный ввод'
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
    """Сериализатор списка модели `User` для `Djoser`."""
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

    def get_is_subscribed(self, obj):
        """Проверка подписки."""
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Follow.objects.filter(
            user=user,
            author=obj.id,
        ).exists()


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор модели `Follow`."""
    email = serializers.EmailField(
        source='author.email',
        read_only=True
    )
    id = serializers.IntegerField(
        source='author.id',
        read_only=True
    )
    username = serializers.CharField(
        source='author.username',
        read_only=True
    )
    first_name = serializers.CharField(
        source='author.first_name',
        read_only=True
    )
    last_name = serializers.CharField(
        source='author.last_name',
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

    def get_is_subscribed(self, obj):
        """Проверка подписки."""
        return Follow.objects.filter(
            user=obj.user,
            author=obj.author,
        ).exists()

    def get_recipes(self, obj):
        """Получение рецептов пользователя"""
        limit = self.context.get(
            'request'
        ).query_params.get('recipes_limit')
        recipe = Recipe.objects.filter(
            author=obj.author
        )
        if limit:
            recipe = recipe[:int(limit)]
        return FavoriteShopAndUserSerializer(recipe, many=True).data

    def get_recipes_count(self, obj):
        """Получение количества рецептов пользователя."""
        return Recipe.objects.filter(
            author=obj.author
        ).count()
