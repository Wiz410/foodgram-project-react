from rest_framework.pagination import PageNumberPagination


class RecipeAndSubscriptionPagination(PageNumberPagination):
    """Пагинация для рецептов и подписок."""
    page_size_query_param = 'limit'
