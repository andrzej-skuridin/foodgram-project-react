from rest_framework import serializers

from recipes.models import Ingredient, RecipeIngredient, Recipe, RecipeTag, Tag


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
    is_favorite = serializers.BooleanField()

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
        fields = ('name', 'ingredients', 'is_favorite', 'text', 'tags')


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
    tags = serializers.ListField(min_length=1) #TagCreateInRecipeSerializer(many=True)

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
        fields = ('name', 'ingredients', 'text', 'tags')
