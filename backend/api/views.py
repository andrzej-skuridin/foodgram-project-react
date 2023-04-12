from django.shortcuts import get_object_or_404
from rest_framework import filters, serializers
from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from api.permissions import (
    RecipePermission,
)
from api.serializers import (
    TagSerializer,
    IngredientSerializer,
    FavoriteSerializer,
    RecipeListRetrieveSerializer,
)
from recipes.models import (
    Tag,
    Ingredient,
    Recipe, Favorite
)


class TagViewSet(mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = (AllowAny,)


class IngredientViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    permission_classes = (AllowAny,)

    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [RecipePermission]

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeListRetrieveSerializer  # GET/list
        return RecipeListRetrieveSerializer
    #     if self.action in ('retrieve', 'destroy'):
    #         return RecipeRetrieveSerializer  # GET/retrieve or ?POST/destroy?
    #     if self.action == 'update':
    #         return RecipeUpdateSerializer  # POST/create or PATCH/update


class FavoriteViewSet(mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = IsAuthenticated,

    def get_queryset(self):
        recipe_id = self.kwargs.get('recipe_id')
        new_queryset = Favorite.objects.filter(recipe_key=recipe_id)
        return new_queryset

    # не работает удаление из избранного!
    def perform_destroy(self, instance):
        recipe_id = self.kwargs.get('recipe_id')

        # проверка, что такой Favorite уже в БД
        queryset = Favorite.objects.filter(
            follower=self.request.user,
            recipe_key=recipe_id
        )
        if len(queryset) == 0:
            raise serializers.ValidationError(
                'Этот рецепт отсутствует в Избранном!'
            )

        Favorite.objects.filter(recipe_key=recipe_id).delete()

    def perform_create(self, serializer):
        recipe_id = self.kwargs.get('recipe_id')
        recipe = get_object_or_404(Recipe, id=recipe_id)

        # проверка, что такого Favorite уже нет в БД
        queryset = Favorite.objects.filter(
            follower=self.request.user,
            recipe_key=recipe_id
        )
        if len(queryset) > 0:
            raise serializers.ValidationError(
                'Этот рецепт уже есть в Избранном!'
            )

        # запись нового объекта Favorite
        serializer.save(follower=self.request.user,
                        name=recipe.name,
                        cooking_time=recipe.cooking_time,
                        recipe_key=recipe
                        )
