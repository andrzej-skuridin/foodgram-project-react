from django_filters import rest_framework as filters

from recipes.models import Recipe


class RecipeFilter(filters.FilterSet):
    tags = filters.CharFilter(field_name='tags__slug')
    is_favorited = filters.BooleanFilter

    class Meta:
        fields = ('tags',)
        model = Recipe
