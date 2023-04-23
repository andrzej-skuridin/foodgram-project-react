from django.shortcuts import render, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets, serializers, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.filters import RecipeFilter
from api.permissions import IsOwnerOrReadOnly
from api.serializers import RecipeListSerializer, RecipeCreateUpdateSerializer, IngredientSerializer, TagSerializer, \
    UserInSubscriptionSerializer, FavoriteSerializer
from recipes.models import Recipe, Tag, Ingredient, Favorite
from users.models import Subscription, User


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = (
        'tags',
        'is_favorited'  # не работает!
    )
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return RecipeCreateUpdateSerializer

        return RecipeListSerializer

    def get_queryset(self):
        qs = Recipe.objects.add_user_annotations(self.request.user.pk)

        # Фильтры из GET-параметров запроса, например.
        author = self.request.query_params.get('author', None)
        if author:
            qs = qs.filter(author=author)

        return qs


class IngredientViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    permission_classes = (AllowAny,)

    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)


class TagViewSet(mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = (AllowAny,)


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

    def create(self, request, *args, **kwargs):  # perform_create
        author_id = self.kwargs.get('user_id')
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
        Subscription.objects.create(
            follower=self.request.user,
            author_id=author_id
        )
        return Response(status=status.HTTP_201_CREATED)

    @action(detail=False,
            methods=('delete',),
            permission_classes=IsAuthenticated,
            # url /subscribe/ обрабатывается в urls.py, видимо поэтому
            # работает при таком пути
            url_path=r'users/(?P<user_pk>\d+)/',
            )
    def delete(self, request, *args, **kwargs):
        # почему-то называть надо именно delete
        # (сработает ли perform_destroy, проверить)
        # стандартный viewset разрешает метод delete только на something/id/
        # поэтому если /something/something_else, придётся @action писать
        author_id = self.kwargs.get('user_id')

        # проверка, что такая Subscription существует в БД
        queryset = Subscription.objects.filter(
            follower=self.request.user,
            author_id=author_id
        )
        if len(queryset) == 0:
            raise serializers.ValidationError(
                'Вы не подписаны на этого автора!'
            )

        Subscription.objects.filter(
            follower=self.request.user, author_id=author_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FavoriteViewSet(viewsets.ModelViewSet):
    http_method_names = ['post', 'delete']
    serializer_class = FavoriteSerializer
    permission_classes = IsAuthenticated,

    def get_queryset(self):
        recipe_id = self.kwargs.get('recipe_id')
        new_queryset = Favorite.objects.filter(
            recipe=recipe_id)
        return new_queryset

    @action(detail=False,
            methods=('delete',),
            permission_classes=IsAuthenticated,
            url_path='')
    def delete(self, request, *args, **kwargs):
        # стандартный viewset разрешает метод delete только на something/id/
        # поэтому если /something/something_else, придётся @action писать
        recipe_id = self.kwargs.get('recipe_id')

        # проверка, что такой Favorite существует в БД
        queryset = Favorite.objects.filter(
            follower=self.request.user,
            recipe=recipe_id
        )
        if len(queryset) == 0:
            raise serializers.ValidationError(
                'Этот рецепт отсутствует в Избранном!'
            )

        Favorite.objects.filter(recipe=recipe_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_create(self, serializer):
        recipe_id = self.kwargs.get('recipe_id')
        recipe = get_object_or_404(Recipe, id=recipe_id)

        # проверка, что такого Favorite уже нет в БД
        queryset = Favorite.objects.filter(
            follower=self.request.user,
            recipe=recipe_id
        )
        if len(queryset) > 0:
            raise serializers.ValidationError(
                'Этот рецепт уже есть в Избранном!'
            )

        # запись нового объекта Favorite
        serializer.save(follower=self.request.user,
                        #ame=recipe.name,
                        #cooking_time=recipe.cooking_time,
                        recipe=recipe
                        )

        return Response(status=status.HTTP_201_CREATED)
