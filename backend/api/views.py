import csv
from collections import defaultdict

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.filters import RecipeFilter, IngredientFilter
from api.permissions import IsOwnerOrReadOnly
from api.serializers import (
    FavoriteSerializer,
    IngredientSerializer,
    RecipeCreateUpdateSerializer,
    RecipeListSerializer,
    ShoppingCartSerializer,
    SubscriptionSerializer,
    TagSerializer,
    UserInSubscriptionSerializer,
    UserListRetrieveSerializer,
)
from recipes.models import (
    Favorite,
    Ingredient,
    Recipe,
    RecipeIngredient,
    ShoppingCart,
    Tag,
    RecipeTag,
)
from users.models import Subscription, User


class MeViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """Костыль против ошибки при обращении анонима к эндпоинту /me"""

    permission_classes = (IsAuthenticated,)
    serializer_class = UserListRetrieveSerializer
    pagination_class = None

    def get_queryset(self):
        new_queryset = User.objects.filter(id=self.request.user.pk)
        return new_queryset

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self,
            'subscriptions': set(
                Subscription.objects.filter(
                    follower_id=self.request.user
                ).values_list('author_id', flat=True)
            )
        }


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = (IsOwnerOrReadOnly,)

    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    filterset_fields = (
        'tags',
        'is_in_shopping_cart',
        'author',  # по id работает из коробки, но пусть будет явно
        'is_favorited',
    )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return RecipeCreateUpdateSerializer

        return RecipeListSerializer

    def get_serializer_context(self):
        if self.request.user.is_authenticated:
            return {
                'request': self.request,
                'format': self.format_kwarg,
                'view': self,
                'recipe-tag':
                    RecipeTag.objects.filter(
                        recipe_id=self.kwargs.get('pk')
                    ).all(),
                'recipe-ingredient':
                    RecipeIngredient.objects.filter(
                        recipe_id=self.kwargs.get('pk')
                    ).all(),
                'is_favorited':
                    set(
                        Favorite.objects.filter(
                            follower_id=self.request.user
                        ).values_list('recipe_id', flat=True)
                    ),
                'is_in_shopping_cart':
                    set(
                        ShoppingCart.objects.filter(
                            client_id=self.request.user
                        ).values_list('recipe_id', flat=True)
                    ),
            }
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self,
            'recipe-tag':
                RecipeTag.objects.filter(
                    recipe_id=self.kwargs.get('pk')
                ).all(),
            'recipe-ingredient':
                RecipeIngredient.objects.filter(
                    recipe_id=self.kwargs.get('pk')
                ).all(),
            'is_favorited': False,
            'is_in_shopping_cart': False,
        }

    def get_queryset(self):
        new_queryset = Recipe.objects.add_user_annotations(
            self.request.user.pk
        )

        # Фильтры из GET-параметров запроса, например.
        author = self.request.query_params.get('author', None)
        if author:
            new_queryset = new_queryset.filter(author=author)

        return new_queryset

    @action(
        detail=False,
        methods=('get',),
        permission_classes=(IsAuthenticated,),
        serializer_class=None,
        url_path='',
    )
    def download_shopping_cart(self, request):
        client = self.request.user
        shopping_cart_objects = ShoppingCart.objects.filter(
            client=client
        ).all()
        shopping_list = defaultdict()

        if len(shopping_cart_objects) < 1:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        ingredients = RecipeIngredient.objects.filter(
            recipe__in_shopping_list__client_id=client
        ).values_list(
            'ingredient__name', 'ingredient__measurement_unit', 'amount'
        )

        for name, unit, amount in ingredients:
            if name not in shopping_list.keys():
                shopping_list[name] = {
                    'measurement_unit': unit,
                    'amount': amount,
                }
            else:
                shopping_list[name]['amount'] += amount

        response = HttpResponse(
            content_type='text/csv',
            headers={
                'Content-Disposition':
                    'attachment; filename="shopping_list.csv"'
            },
        )

        writer = csv.writer(response)

        array_of_rows = list()

        for name, vals in shopping_list.items():
            array_of_rows.append(
                (name, vals['measurement_unit'], vals['amount'])
            )
        for row in array_of_rows:
            writer.writerow(row)

        return response


class IngredientViewSet(
    ModelViewSet,
    # mixins.ListModelMixin,
    # mixins.RetrieveModelMixin,
    # viewsets.GenericViewSet
):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    pagination_class = None

    filter_backends = (IngredientFilter,)
    search_fields = ('^name',)
    # search_fields = ('^name',)
    # filterset_class = (IngredientFilter,)
    # filterset_fields = ('^name',)


class TagViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = (AllowAny,)


class SubscriptionViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'delete']
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action not in ('create',):
            return UserInSubscriptionSerializer
        return SubscriptionSerializer

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self,
            'subscriptions': set(
                Subscription.objects.filter(
                    follower_id=self.request.user
                ).values_list('author_id', flat=True)
            ),
        }

    def get_queryset(self):
        me = self.request.user
        # этот queryset выдаёт набор id авторов, на которых подписан пользователь
        author_id_queryset = (
            Subscription.objects.filter(follower=me)
            .values_list('author_id', flat=True)
            .order_by('id')
        )
        # см. документацию по Field lookups из object.filter
        new_queryset = User.objects.filter(id__in=author_id_queryset)
        return new_queryset

    def perform_create(self, serializer):
        author_id = self.kwargs.get('user_id')
        # проверка, что такого Subscription уже нет в БД
        queryset = Subscription.objects.filter(
            follower=self.request.user, author_id=author_id
        )

        if len(queryset) > 0:
            raise serializers.ValidationError(
                'Вы уже подписаны на этого автора!'
            )

        if User.objects.get(id=author_id) == self.request.user:
            raise serializers.ValidationError('Нельзя подписываться на себя!')

        author_obj = User.objects.get(id=author_id)
        print(author_obj)

        # запись нового объекта Subscription (new!)
        serializer.save(
            follower=self.request.user,
            author_id=author_id,
        )

        return Response(status=status.HTTP_201_CREATED)

    @action(
        detail=False,
        methods=('delete',),
        permission_classes=IsAuthenticated,
        url_path=r'users/(?P<user_pk>\d+)/',
        url_name='subscription-delete',
    )
    def delete(self, request, *args, **kwargs):
        author_id = self.kwargs.get('user_id')

        # проверка, что такая Subscription существует в БД
        queryset = Subscription.objects.filter(
            follower=self.request.user, author_id=author_id
        )
        if len(queryset) == 0:
            raise serializers.ValidationError(
                'Вы не подписаны на этого автора!'
            )

        Subscription.objects.filter(
            follower=self.request.user, author_id=author_id
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FavoriteViewSet(viewsets.ModelViewSet):
    http_method_names = ['post', 'delete']
    serializer_class = FavoriteSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        recipe_id = self.kwargs.get('recipe_id')
        new_queryset = Favorite.objects.filter(recipe=recipe_id)
        return new_queryset

    @action(
        detail=False,
        methods=('delete',),
        permission_classes=IsAuthenticated,
        url_path='',
        url_name='favorite-delete',
    )
    def delete(self, request, *args, **kwargs):
        # стандартный viewset разрешает метод delete только на something/id/
        # поэтому если /something/something_else/, придётся @action писать
        recipe_id = self.kwargs.get('recipe_id')

        # проверка, что такой Favorite существует в БД
        queryset = Favorite.objects.filter(
            follower=self.request.user, recipe=recipe_id
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
            follower=self.request.user, recipe=recipe_id
        )
        if len(queryset) > 0:
            raise serializers.ValidationError(
                'Этот рецепт уже есть в Избранном!'
            )

        # запись нового объекта Favorite
        serializer.save(follower=self.request.user, recipe=recipe)

        return Response(status=status.HTTP_201_CREATED)


class ShoppingCartViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    http_method_names = ['post', 'delete']
    permission_classes = (IsAuthenticated,)
    pagination_class = None
    serializer_class = ShoppingCartSerializer

    def get_queryset(self):
        new_queryset = ShoppingCart.objects.filter(client=self.request.user)
        return new_queryset

    @action(
        detail=False,
        methods=('delete',),
        permission_classes=IsAuthenticated,
        serializer_class=ShoppingCartSerializer,
        url_path='',
    )
    def delete(self, request, *args, **kwargs):
        recipe_id = self.kwargs.get('recipe_id')

        # проверка, что такой ShoppingCart существует в БД
        queryset = ShoppingCart.objects.filter(
            client=self.request.user, recipe=recipe_id
        )
        if len(queryset) == 0:
            raise serializers.ValidationError(
                'Этот рецепт отсутствует в списке покупок!'
            )

        ShoppingCart.objects.filter(
            client=self.request.user, recipe=recipe_id
        ).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_create(self, serializer):
        recipe_id = self.kwargs.get('recipe_id')
        recipe = get_object_or_404(Recipe, id=recipe_id)

        # проверка, что такого ShoppingCart уже нет в БД
        queryset = ShoppingCart.objects.filter(
            client=self.request.user, recipe=recipe_id
        )
        if len(queryset) > 0:
            raise serializers.ValidationError(
                'Этот рецепт уже есть в списке покупок!'
            )

        # запись нового объекта ShoppingCart
        serializer.save(
            client=self.request.user,
            recipe=recipe,
        )

        return Response(status=status.HTTP_201_CREATED)
