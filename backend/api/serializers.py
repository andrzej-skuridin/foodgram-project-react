from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from recipes.models import Tag, Ingredient
from users.models import User


class UserGETSerializer(serializers.ModelSerializer):
    # is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            # 'is_subscribed'
        )

    # def is_subscribed(self, data, request):
    #     current_user = request.user.username
    #     author = data['username']
    #     return current_user == author


class UserPOSTSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password'
        )

    def validate_password(self, value: str) -> str:
        # Без хэширования пароля (согласно модели он просто текст) не работает JWT.
        return make_password(value)


# class PasswordChangeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('password',)
#
#     def validate_password(self, value: str) -> str:
#         # Без хэширования пароля (согласно модели он просто текст) не работает JWT.
#         return make_password(value)


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = '__all__'