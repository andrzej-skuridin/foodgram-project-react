from django.core.exceptions import ValidationError


def validate_cooking_time(value):
    if value < 1:
        raise ValidationError(
            f'Время готовки не может быть меньше 1 минуты.')
    return value
