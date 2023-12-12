from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Follow

OBJECT_PER_PAGE: int = 10
User = get_user_model()
admin.site.empty_value_display = 'Не задано'


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Регистрация модели `User` для админки."""
    list_display = [
        'username',
        'email',
        'first_name',
        'last_name',
    ]
    list_editable = [
        'email',
        'first_name',
        'last_name',
    ]
    filter_horizontal = ['groups', 'user_permissions']
    list_per_page = OBJECT_PER_PAGE
    ordering = [
        'id',
        'username',
    ]

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'author',
    ]
    list_editable = [
        'author',
    ]
    list_per_page = OBJECT_PER_PAGE
    ordering = [
        'user',
    ]
