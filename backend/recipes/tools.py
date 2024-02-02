from . import constants as con


def minutes_to_hours(minutes: int) -> str:
    """Перевод минут в часы с готовым текстом.

    Args:
        - minutes (int): Времия в минутах.

    Returns:
        - str: Если 1 час и более  текст формата `(_ часов)`
        или пустой текст.
    """
    res: int = minutes // con.TOOL_MIN_IN_H
    if res > 0:
        return f' ({res} часов) '
    return ''
