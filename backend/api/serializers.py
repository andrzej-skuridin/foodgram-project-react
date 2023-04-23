from rest_framework import serializers

from recipes.models import Ingredient, RecipeIngredient, Recipe, RecipeTag, Tag, User, Favorite
from users.models import Subscription


class UserListRetrieveSerializer(serializers.ModelSerializer):
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


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """Сериализатор таблицы связи."""

    name = serializers.StringRelatedField(
        source='ingredient.name'
    )
    measurement_unit = serializers.StringRelatedField(
        source='ingredient.measurement_unit'
    )
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient',
        queryset=Ingredient.objects.all()
    )

    class Meta:
        model = RecipeIngredient
        fields = ('amount', 'name', 'measurement_unit', 'id')


class RecipeTagSerializer(serializers.ModelSerializer):
    """Сериализатор таблицы связи."""

    id = serializers.PrimaryKeyRelatedField(
        source='tag',
        queryset=Tag.objects.all()
    )
    name = serializers.StringRelatedField(
        source='tag.name'
    )
    color = serializers.StringRelatedField(
        source='tag.color'
    )
    slug = serializers.SlugRelatedField(
        source='tag',
        slug_field='slug',
        queryset=Tag.objects.all()
    )

    class Meta:
        model = RecipeTag
        fields = ('id', 'name', 'color', 'slug')


class RecipeListSerializer(serializers.ModelSerializer):
    """Получение списка рецептов."""

    tags = serializers.SerializerMethodField()
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.BooleanField()
    author = UserListRetrieveSerializer()

    def get_ingredients(self, obj):
        """Возвращает отдельный сериализатор."""
        return RecipeIngredientSerializer(
            RecipeIngredient.objects.filter(recipe=obj).all(), many=True
        ).data

    def get_tags(self, obj):
        """Возвращает отдельный сериализатор."""
        return RecipeTagSerializer(
            RecipeTag.objects.filter(recipe_id=obj).all(), many=True
        ).data

    class Meta:
        model = Recipe
        fields = ('name', 'ingredients', 'is_favorited', 'text', 'tags', 'cooking_time', 'id', 'author')


class IngredientCreateInRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиентов в создании рецепта."""

    recipe = serializers.PrimaryKeyRelatedField(read_only=True)
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient',
        queryset=Ingredient.objects.all()
    )
    amount = serializers.IntegerField(write_only=True, min_value=1)

    class Meta:
        model = RecipeIngredient
        fields = ('recipe', 'id', 'amount')


class TagCreateInRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор тегов в создании рецепта."""

    id = serializers.PrimaryKeyRelatedField(
        source='tag',
        queryset=Tag.objects.all()
    )
    recipe = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = RecipeTag
        fields = ('recipe', 'id')


class RecipeCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор создания/обновления рецепта."""

    ingredients = IngredientCreateInRecipeSerializer(many=True)
    tags = serializers.ListField(min_length=1)

    def validate_ingredients(self, value):
        if len(value) < 1:
            raise serializers.ValidationError("Добавьте хотя бы один ингредиент.")
        return value

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)

        create_ingredients = [
            RecipeIngredient(
                recipe=recipe,
                ingredient=ingredient['ingredient'],
                amount=ingredient['amount']
            )
            for ingredient in ingredients
        ]

        create_tags = [
            RecipeTag(
                recipe=recipe,
                tag=Tag.objects.get(id=tag),
            )
            for tag in tags
        ]

        RecipeIngredient.objects.bulk_create(
            create_ingredients
        )

        RecipeTag.objects.bulk_create(
            create_tags
        )

        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients', None)
        if ingredients is not None:
            instance.ingredients.clear()

            create_ingredients = [
                RecipeIngredient(
                    recipe=instance,
                    ingredient=ingredient['ingredient'],
                    amount=ingredient['amount']
                )
                for ingredient in ingredients
            ]
            RecipeIngredient.objects.bulk_create(
                create_ingredients
            )
        return super().update(instance, validated_data)

    def to_representation(self, obj):
        """Возвращаем прдеставление в таком же виде, как и GET-запрос."""

        self.fields.pop('ingredients')
        self.fields.pop('tags')

        representation = super().to_representation(obj)

        representation['ingredients'] = RecipeIngredientSerializer(
            RecipeIngredient.objects.filter(recipe=obj).all(), many=True
        ).data

        representation['tags'] = RecipeTagSerializer(
            RecipeTag.objects.filter(recipe=obj).all(), many=True
        ).data

        return representation

    class Meta:
        model = Recipe
        fields = ('name', 'ingredients', 'text', 'tags', 'cooking_time')


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class UserInSubscriptionSerializer(UserListRetrieveSerializer):
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


class SubscriptionSerializer(serializers.ModelSerializer):
    author = UserInSubscriptionSerializer(many=False, required=True)

    class Meta:
        model = Subscription
        fields = '__all__'


class FavoriteSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()

    name = serializers.SerializerMethodField()
    # image TBA
    cooking_time = serializers.SerializerMethodField()

    class Meta:
        model = Favorite
        fields = (
            'id',
            'name',
            'cooking_time',
            # 'image' TBA
        )

    def get_id(self, data):
        return int(self.context.get('request').parser_context.get('kwargs').get(
            'recipe_id'))

    def get_name(self, data):
        recipe_id = int(self.context.get('request').parser_context.get('kwargs').get(
            'recipe_id'))
        return Recipe.objects.get(id=recipe_id).name

    def get_cooking_time(self, data):
        recipe_id = int(self.context.get('request').parser_context.get('kwargs').get(
            'recipe_id'))
        return Recipe.objects.get(id=recipe_id).cooking_time
