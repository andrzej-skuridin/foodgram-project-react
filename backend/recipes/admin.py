from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import (
    Favorite,
    Ingredient,
    Recipe,
    RecipeIngredient,
    RecipeTag,
    ShoppingCart,
    Tag,
)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'slug',
    )
    search_fields = (
        'id',
        'name',
        'slug',
    )
    list_filter = (
        'name',
        'slug',
    )


@admin.register(Ingredient)
class IngredientAdmin(ImportExportModelAdmin):
    list_display = (
        'id',
        'name',
        'measurement_unit',
    )
    search_fields = ('id', 'name', 'measurement_unit')
    list_filter = ('name',)


class IngredientResource(resources.ModelResource):

    class Meta:
        model = Ingredient


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'tags',
        'ingredients',
        'author',
        'fav_counter'
    )
    search_fields = ('id', 'name', 'author', 'tags')
    list_filter = ('name',)

    def fav_counter(self, obj):
        return Favorite.objects.filter(recipe=obj).count()

    fav_counter.short_description = 'В избранном'


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'ingredient', 'amount')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'follower',
        'recipe',
    )
    search_fields = (
        'id',
        'follower',
        'recipe',
    )
    list_filter = (
        'follower',
        'recipe',
    )


@admin.register(RecipeTag)
class RecipeTagAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'tag',
        'recipe',
    )


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'client',
        'recipe',
    )
    search_fields = (
        'client',
        'recipe',
    )
    list_filter = (
        'client',
        'recipe',
    )
