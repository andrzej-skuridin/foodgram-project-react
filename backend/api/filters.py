import django_filters
from django_filters import rest_framework as filters

from recipes.models import Recipe, Ingredient


class RecipeFilter(filters.FilterSet):
    tags = filters.CharFilter(field_name='tags__slug')
    is_favorited = filters.BooleanFilter(
        field_name='is_favorited'
    )
    is_in_shopping_cart = filters.BooleanFilter(
        field_name='is_in_shopping_cart'
    )

    class Meta:
        fields = ('tags',)
        model = Recipe


class IngredientFilter(django_filters.FilterSet):
    name = filters.CharFilter(lookup_expr='isstartswith')

    class Meta:
        model = Ingredient
        fields = ('name',)

