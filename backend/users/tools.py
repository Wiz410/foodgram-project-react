from .models import Follow


def get_follow(user, id: int) -> bool:
    if user.is_anonymous:
        return False
    return Follow.objects.filter(
        user=user,
        following=id
    ).exists()
