from django_filters import rest_framework as filters

from backend.foodgram.recipes.models import Recipe


class RecipeFilter(filters.FilterSet):
    # is_favorited
    # is_in_shopping_cart
    tags = filters.CharFilter(field_name='tag__slug', lookup_expr='icontains')
    author = filters.CharFilter(field_name='author__id')

    class Meta:
        model = Recipe
        fields = '__all__'
