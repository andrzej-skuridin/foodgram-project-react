from django.shortcuts import render
from rest_framework import filters
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from api.pagination import PageLimitPagination
from api.serializers import (TagSerializer,
                             # PasswordChangeSerializer,
                             UserPOSTSerializer,
                             UserGETSerializer,
                             IngredientSerializer,
                             )
from recipes.models import Tag, Ingredient
from users.models import User


class UserViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.CreateModelMixin,
                  viewsets.GenericViewSet):
    """Обрабатывает всё, что касается пользователя, кроме связанного с токеном"""
    queryset = User.objects.all()
    pagination_class = PageLimitPagination
    permission_classes = (AllowAny,)

    def get_serializer_class(self):
        if self.action == 'create':
            return UserPOSTSerializer
        return UserGETSerializer

    @action(
        methods=('get',),
        detail=False,  # а почему не True, интересно? Возможно, потому что из всех пользователей ищем себя?
        permission_classes=(IsAuthenticated,),
    )
    def me(self, request):
        """Выдаёт информацию о текущем пользователе"""
        serializer = UserGETSerializer(request.user)
        return Response(serializer.data)

    # @action(
    #     methods=('post',),
    #     detail=False,
    #     permission_classes=(IsAuthenticated,),
    # )
    # def set_password(self, request):
    #     """Смена пароля текущего пользователя"""
    #     serializer = PasswordChangeSerializer(  # не соответствует модели!
    #         request.user,  # тут instance той модели, для которой сериализатор
    #         data=request.data,
    #         partial=False  # потому что у сериализатора только одно поле, пароль
    #     )
    #     serializer.is_valid(raise_exception=True)  # проверяем, что там насовали в новый пароль
    #     return Response(status=status.HTTP_204_NO_CONTENT)


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
