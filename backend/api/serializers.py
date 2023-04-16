from django.contrib.auth.hashers import make_password
from django.core.validators import MaxLengthValidator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.fields import CharField
from rest_framework.permissions import IsAuthenticated, AllowAny

from recipes.models import (
    Tag,
    Ingredient,
    Recipe, IngredientRecipe, Favorite
)
from users.models import User, Subscription


class UserGETSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, data):
        current_user = self.context.get('request').user.id
        author = data.id
        return Subscription.objects.filter(
            follower_id=current_user, author_id=author).exists()


class UserGETmeSerializer(UserGETSerializer):
    """Этот сериалайзер должен не допускать анонима к endpoint /me/,
    но почему-то всё равно допускает и выдаёт ошибку из-за незаполнения полей
    см. settings"""
    permission_classes = IsAuthenticated,


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientRecipeSerializer(serializers.ModelSerializer):
    # я знаю, что это дикое извращение, но иначе у меня не получается
    # понимаю, что вместо метод-филдов нужно сериализатор применить,
    # но что-то он не применяется
    measurement_unit = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    class Meta:
        model = IngredientRecipe
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount',
        )

    def get_measurement_unit(self, obj):
        ingredient_id = obj.get('ingredient_id')
        ingredient_info = Ingredient.objects.filter(id=ingredient_id)
        # first() иначе вернёт в виде списка из 1 элемента
        return ingredient_info.values_list('measurement_unit', flat=True).first()

    def get_name(self, obj):
        ingredient_id = obj.get('ingredient_id')
        ingredient_info = Ingredient.objects.filter(id=ingredient_id)
        # first() иначе вернёт в виде списка из 1 элемента
        return ingredient_info.values_list('name', flat=True).first()


class RecipeListRetrieveSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=True)
    author = UserGETSerializer(many=False, required=True)
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    # is_in_shopping_cart

    class Meta:
        model = Recipe
        fields = '__all__'

    def get_is_favorited(self, obj):
        if Favorite.objects.filter(recipe_key_id=obj.id).exists():
            return self.context.get('request').user.id == get_object_or_404(
                Favorite, recipe_key_id=obj.id).follower.id
        return False

    def get_ingredients(self, obj):
        ings = IngredientRecipe.objects.filter(recipe_id=obj.id).all().values()
        return IngredientRecipeSerializer(ings, many=True).data


class UserInSubscriptionSerializer(UserGETSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )

    def get_recipes(self, data):
        author_id = data.id
        recipes_queryset = Recipe.objects.filter(author_id=author_id)
        return recipes_queryset.values()

    def get_recipes_count(self, data):
        return len(Recipe.objects.filter(author_id=data.id))


class RecipeCreatePatchSerializer(serializers.ModelSerializer):
    """TBA"""

    class Meta:
        model = Recipe
        fields = '__all__'


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ('id',
                  'name',
                  # 'image',
                  'cooking_time',
                  )


class SubscriptionSerializer(serializers.ModelSerializer):
    author = UserInSubscriptionSerializer(many=False, required=True)

    class Meta:
        model = Subscription
        fields = '__all__'
