from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter

from recipes.models import Recipe


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

class IngredientFilter(SearchFilter):
    search_param = 'name'
