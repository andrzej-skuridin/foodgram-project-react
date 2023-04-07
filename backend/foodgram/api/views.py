from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, mixins, status, generics

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated

from backend.foodgram.api.filters import RecipeFilter
from backend.foodgram.api.serializers import (RecipeListSerializer,
                                              TagSerializer,
                                              RecipeRetrieveSerializer,
                                              RecipePostPatchSerializer,
                                              IngredientSerializer, UserSerializer, PasswordChangeSerializer
                                              )
from backend.foodgram.recipes.models import Recipe, Tag, Favorite
from rest_framework.response import Response

from backend.foodgram.users.models import User


# Работа с пользователями
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """Получение токена"""
    pass


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """Удаление токена текущего пользователя"""
    pass


class UserViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.CreateModelMixin,
                  viewsets.GenericViewSet):
    """Обрабатывает всё, что касается пользователя, кроме связанного с токеном"""
    queryset = User.objects.all().order_by('pk')
    serializer_class = UserSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('id')
        new_queryset = Tag.objects.filter(id=user_id)
        return new_queryset

    @action(
        methods=['get'],
        detail=False,  # а почему не True, интересно?
        # permission_classes=(IsAuthenticated,),
    )
    def me(self, request):
        """Выдаёт информацию о текущем пользователе"""
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    @action(
        methods=['post'],
        detail=False,
        # permission_classes=(IsAuthenticated,),
    )
    def set_password(self, request):
        """Смена пароля текущего пользователя"""
        serializer = PasswordChangeSerializer(
            request.user,  # тут instance той модели, для которой сериализатор
            data=request.data,
            partial=False  # потому что у сериализатора только одно поле, пароль
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role)  # это для чего? что за role?
        return Response(serializer.data, status=status.HTTP_200_OK)


class TagViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    serializer_class = TagSerializer

    def get_queryset(self):
        tag_id = self.kwargs.get('id')
        new_queryset = Tag.objects.filter(id=tag_id)
        return new_queryset


class IngredientViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    serializer_class = IngredientSerializer
    search_fields = ('^name',)

    def get_queryset(self):
        ingredient_id = self.kwargs.get('id')
        new_queryset = Tag.objects.filter(id=ingredient_id)
        return new_queryset


class FavoriteViewSet(mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):

    def perform_create(self, serializer):
        favorite_id = self.kwargs.get('id')
        new_favorite = get_object_or_404(Favorite, id=favorite_id)
        serializer.save(user=self.request.user, favorite=new_favorite)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()

    # permission_classes = [IsAdminOrSuperUserOrReadOnly]

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('author',
                        # 'is_favorited',
                        # 'is_in_shopping_cart',
                        'tag')
    filterset_class = RecipeFilter

    # def perform_create(self, serializer):
    #     favorite_id = self.kwargs.get('id')
    #     new_favorite = get_object_or_404(Favorite, id=favorite_id)
    #     serializer.save(author=self.request.user, favorite=new_favorite)

    def get_serializer_class(self):
        if self.action == 'list':
            return RecipeListSerializer
        if self.action == 'retrieve':
            return RecipeRetrieveSerializer
        return RecipePostPatchSerializer
