from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, serializers, status
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from api.permissions import (
    RecipePermission,
)
from api.serializers import (
    TagSerializer,
    IngredientSerializer,
    FavoriteSerializer,
    RecipeListRetrieveSerializer,
    RecipeCreatePatchSerializer,
    SubscriptionSerializer,
    UserGETSerializer,
    UserInSubscriptionSerializer,
)
from recipes.models import (
    Tag,
    Ingredient,
    Recipe, Favorite
)
from users.models import Subscription, User


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

    filter_backends = (DjangoFilterBackend,)  # нужно написать свой фильтр, этот не работает
    search_fields = ('author_username',
                     'is_favorited',
                     'tags',
                     # 'is_in_shopping_cart',
                     )

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeListRetrieveSerializer  # GET/list
        if self.action in ('create', 'update'):
            return RecipeCreatePatchSerializer  # сломано
        return RecipeListRetrieveSerializer


class FavoriteViewSet(viewsets.ModelViewSet):
    http_method_names = ['post', 'delete']
    serializer_class = FavoriteSerializer
    permission_classes = IsAuthenticated,
    queryset = Favorite.objects.all()

    # Это раскоментить для тестов через GET
    # def get_queryset(self):
    #     recipe_id = self.kwargs.get('recipe_id')
    #     new_queryset = Favorite.objects.filter(recipe_key=recipe_id)
    #     return new_queryset

    # не работает удаление из избранного!
    def perform_destroy(self, instance):
        recipe_id = self.kwargs.get('recipe_id')

        # проверка, что такой Favorite существует в БД
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


class SubscriptionViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'delete']
    permission_classes = IsAuthenticated,
    serializer_class = UserInSubscriptionSerializer

    def get_queryset(self):
        me = self.request.user
        # этот queryset выдаёт набор id авторов, на которых подписан пользователь
        author_id_queryset = Subscription.objects.filter(follower=me).values_list(
            'author_id', flat=True).order_by('id')
        # см. документацию по Field lookups из object.filter
        new_queryset = User.objects.filter(id__in=author_id_queryset)
        return new_queryset

    @action(
        methods=('post',),
        url_path=r'users/(?P<user_pk>\d+)',
        detail=False,
    )
    def subscribe(self, serializer):  # perform_create
        author_id = self.kwargs.get('user_id')
        author = get_object_or_404(User, id=author_id)
        # проверка, что такого Subscription уже нет в БД
        queryset = Subscription.objects.filter(
            follower=self.request.user,
            author_id=author_id
        )
        if len(queryset) > 0:
            raise serializers.ValidationError(
                'Вы уже подписаны на этого автора!'
            )
        # запись нового объекта Subscription
        serializer.save(follower=self.request.user,
                        author=author
                        )
