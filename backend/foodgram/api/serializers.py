from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from rest_framework.pagination import LimitOffsetPagination

from backend.foodgram.recipes.models import Recipe, Favorite, Tag, Ingredient
from backend.foodgram.users.models import User


class RegisterDataSerializer(serializers.Serializer):
    username = serializers.RegexField(
        max_length=150,
        required=True,
        regex=r"^[\w.@+-]+\Z",
        # validators=[validate_username]
    )
    email = serializers.EmailField(
        max_length=254,
        required=True
    )

    def validate(self, data):
        if User.objects.filter(username=data['username'],
                               email=data['email']).exists():
            return data
        if (User.objects.filter(username=data['username']).exists()
                or User.objects.filter(email=data['email']).exists()):
            raise serializers.ValidationError(
                'Почта или имя уже использовались')
        return data


class PasswordChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('password',)


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        exclude = ('role',)

    def is_subscribed(self, data):
        current_user = CurrentUserDefault()
        author = data['username']
        return current_user == author


class TagSerializer:

    class Meta:
        model = Tag
        fields = '__all__'
        read_only_fields = '__all__'


class IngredientSerializer:

    class Meta:
        model = Ingredient
        fields = '__all__'


class RecipeListSerializer(serializers.ModelSerializer):
    pagination_class = LimitOffsetPagination

    tags = TagSerializer()
    author = UserSerializer(many=False, required=True)
    ingredients = IngredientSerializer()
    # is_favorited = serializers.SerializerMethodField()
    # is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = '__all__'

    # def is_favorited(self, data):
    #     return Favorite.objects.filter(
    #         user=CurrentUserDefault(),
    #         recipe=
    #     ).exists()

    # def is_in_shopping_cart(self):
    #     pass


class RecipeRetrieveSerializer(serializers.ModelSerializer):
    pagination_class = None

    tags = TagSerializer()
    author = UserSerializer(many=False, required=True)
    ingredients = IngredientSerializer()
    # is_favorited = serializers.SerializerMethodField()
    # is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = '__all__'

    # def is_favorited(self, data):
    #     return Favorite.objects.filter(
    #         user=CurrentUserDefault(),
    #         recipe=
    #     ).exists()

    # def is_in_shopping_cart(self):
    #     pass


class RecipePostPatchSerializer(serializers.ModelSerializer):
    pagination_class = None

    pass


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'
