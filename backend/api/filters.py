from django_filters import rest_framework as filters

from recipes.models import Recipe


class RecipeFilter(filters.FilterSet):
    tags = filters.CharFilter(field_name='tags__slug')
    # фильтровать немодельные поля можно только если они сделаны через аннотирование
    # если через метод филд, то идём лесом. is_in_shopping_cart надо переделать через аннотирование
    is_favorited = filters.BooleanFilter(
        field_name='is_favorited'
    )  # нельзя это вписывать в мета
    is_in_shopping_cart = filters.BooleanFilter(
        field_name='is_in_shopping_cart'
    )

    class Meta:
        fields = ('tags',)
        model = Recipe
