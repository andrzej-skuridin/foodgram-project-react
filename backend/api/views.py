from rest_framework import filters
from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny

from api.permissions import (
    RecipePermission,
)
from api.serializers import (
    TagSerializer,
    IngredientSerializer,
    RecipeListSerializer,
)
from recipes.models import (
    Tag,
    Ingredient,
    Recipe
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
    # permission_classes = [RecipePermission]
    permission_classes = AllowAny,  # не забыть убрать!
    # serializer_class = RecipeListSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return RecipeListSerializer  # GET/list
        return RecipeListSerializer
    #     if self.action in ('retrieve', 'destroy'):
    #         return RicepeRetriveSerializer  # GET/retrieve or ?POST/destroy?
    #     if self.action == 'update':
    #         return RecipeUpdateSerializer  # POST/create or PATCH/update
