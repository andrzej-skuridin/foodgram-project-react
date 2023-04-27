from django.contrib import admin

from .models import (Recipe,
                     Ingredient,
                     Tag,
                     RecipeIngredient,
                     RecipeTag,
                     Favorite,
                     ShoppingCart
                     )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug',)
    search_fields = ('id', 'name', 'slug',)
    list_filter = ('name', 'slug',)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit',)
    search_fields = ('id', 'name', 'measurement_unit')
    list_filter = ('name',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author', 'fav_counter')
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
    list_display = ('id', 'follower', 'recipe',)
    search_fields = ('id', 'follower', 'recipe',)
    list_filter = ('follower', 'recipe',)


@admin.register(RecipeTag)
class RecipeTagAdmin(admin.ModelAdmin):
    list_display = ('id', 'tag', 'recipe',)


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'recipe',)
    search_fields = ('client', 'recipe',)
    list_filter = ('client', 'recipe',)
