import csv

from django.shortcuts import render, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets, serializers, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
import io
from django.http import FileResponse, HttpResponse
from reportlab.pdfgen import canvas
from django.template import loader

from api.filters import RecipeFilter
from api.permissions import IsOwnerOrReadOnly
from api.serializers import RecipeListSerializer, RecipeCreateUpdateSerializer, IngredientSerializer, TagSerializer, \
    UserInSubscriptionSerializer, FavoriteSerializer, ShoppingCartSerializer
from recipes.models import Recipe, Tag, Ingredient, Favorite, ShoppingCart, RecipeIngredient
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
        new_queryset = Recipe.objects.add_user_annotations(self.request.user.pk)

        # Фильтры из GET-параметров запроса, например.
        author = self.request.query_params.get('author', None)
        if author:
            new_queryset = new_queryset.filter(author=author)

        return new_queryset

    @action(detail=False,
            methods=('get',),
            permission_classes=(IsAuthenticated,),
            serializer_class=None,
            url_path=''  # возможно тут надо будет оказать путь
            )
    def download_shopping_cart(self, request):
        client = self.request.user
        shopping_cart_objects = ShoppingCart.objects.filter(client=client).all()
        shopping_list = dict()

        if len(shopping_cart_objects) < 1:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        ingredients = RecipeIngredient.objects.filter(
            recipe__in_shopping_list__client_id=client
        ).values_list(
            'ingredient__name',
            'ingredient__measurement_unit',
            'amount'
        )

        for item in ingredients:
            name = item[0]
            if name not in shopping_list.items():
                shopping_list[item] = {
                    'measurement_unit': item[1],
                    'amount': item[2]
                }
            else:
                shopping_list[name]['amount'] += item[2]

        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename="shopping_list.csv"'},
        )

        writer = csv.writer(response)
        for item in shopping_list:
            writer.writerow(item)

        return response


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
            # работает при таком пути, возможно и стереть можно,
            # но раз заботает, не чиню
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
        # поэтому если /something/something_else/, придётся @action писать
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
        serializer.save(
            follower=self.request.user,
            recipe=recipe
        )

        return Response(status=status.HTTP_201_CREATED)


class ShoppingCartViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    http_method_names = ['post', 'delete']
    permission_classes = IsAuthenticated,
    pagination_class = None
    serializer_class = ShoppingCartSerializer

    def get_queryset(self):
        new_queryset = ShoppingCart.objects.filter(
            client=self.request.user)
        return new_queryset

    @action(detail=False,
            methods=('delete',),
            permission_classes=IsAuthenticated,
            serializer_class=ShoppingCartSerializer,
            url_path='')
    def delete(self, request, *args, **kwargs):
        # стандартный viewset разрешает метод delete только на something/id/
        # поэтому если /something/something_else/, придётся @action писать
        recipe_id = self.kwargs.get('recipe_id')

        # проверка, что такой ShoppingCart существует в БД
        queryset = ShoppingCart.objects.filter(
            client=self.request.user,
            recipe=recipe_id
        )
        if len(queryset) == 0:
            raise serializers.ValidationError(
                'Этот рецепт отсутствует в списке покупок!'
            )

        ShoppingCart.objects.filter(
            client=self.request.user,
            recipe=recipe_id
        ).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_create(self, serializer):
        recipe_id = self.kwargs.get('recipe_id')
        recipe = get_object_or_404(Recipe, id=recipe_id)

        # проверка, что такого ShoppingCart уже нет в БД
        queryset = ShoppingCart.objects.filter(
            client=self.request.user,
            recipe=recipe_id
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
