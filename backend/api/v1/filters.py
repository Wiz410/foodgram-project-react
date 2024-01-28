import django_filters
from django.contrib.auth import get_user_model
from django.db.models.query import QuerySet

from recipes.models import Recipe

USER = get_user_model()


class RecipeFilter(django_filters.FilterSet):
    """Фильтрация рецептов """
    is_favorited = django_filters.NumberFilter(
        method='get_is_favorited'
    )
    is_in_shopping_cart = django_filters.NumberFilter(
        method='get_is_in_shopping_cart'
    )
    author = django_filters.ModelChoiceFilter(
        queryset=USER.objects.all()
    )
    tags = django_filters.AllValuesMultipleFilter(
        field_name='tags__slug'
    )

    class Meta:
        model = Recipe
        fields = (
            'is_favorited',
            'is_in_shopping_cart',
            'author',
            'tags',
        )

    def get_is_favorited(
        self,
        queryset: QuerySet,
        name: str,
        value: int
    ) -> QuerySet:
        User = self.request.user
        if value == 1 and User.is_authenticated:
            return queryset.filter(favorite_recipe__user=User)
        return queryset

    def get_is_in_shopping_cart(
        self,
        queryset: QuerySet,
        name: str,
        value: int
    ) -> QuerySet:
        User = self.request.user
        if value == 1 and User.is_authenticated:
            return queryset.filter(shop_recipe__user=User)
        return queryset
