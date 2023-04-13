from django.contrib.auth.hashers import make_password
from django.core.validators import MaxLengthValidator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.fields import CharField

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



class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = IngredientRecipe
        fields = '__all__'


class RecipeListRetrieveSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=True)
    author = UserGETSerializer(many=False, required=True)
    ingredients = IngredientSerializer(many=True, required=True)  # так работает, но без amount
    is_favorited = serializers.SerializerMethodField()
    # is_in_shopping_cart
    # ingredients = IngredientRecipeSerializer(many=True, required=True)  # включить, когда буду делать amount

    class Meta:
        model = Recipe
        fields = '__all__'

    def get_is_favorited(self, obj):
        if Favorite.objects.filter(recipe_key_id=obj.id).exists():
            return self.context.get('request').user.id == get_object_or_404(
                Favorite, recipe_key_id=obj.id).follower.id
        return False


class RecipeCreatePatchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = '__all__'

class FavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favorite
        fields = ('id',
                  'name',
                  #'image',
                  'cooking_time',
                  )


class SubscriptionSerializer(serializers.ModelSerializer):
    author = UserGETSerializer(many=False, required=True)

    class Meta:
        model = Subscription
        fields = ('author',)
