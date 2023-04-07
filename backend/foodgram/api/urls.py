from django.urls import include, path

from rest_framework import routers

from backend.foodgram.api.views import (TagViewSet,
                                        RecipeViewSet,
                                        IngredientViewSet,
                                        FavoriteViewSet,
                                        UserViewSet, login, logout,
                                        )

v1_router = routers.DefaultRouter()

v1_router.register(
    prefix='tags',
    basename='tags',
    viewset=TagViewSet
)
v1_router.register(
    prefix='ingredients',
    basename='ingredients',
    viewset=IngredientViewSet
)
v1_router.register(
    prefix='users',
    viewset=UserViewSet,
    basename='users'
)
# v1_router.register(
#     prefix='recipes',
#     basename='recipes',
#     viewset=RecipeViewSet
# )
# v1_router.register(
#     prefix=r'recipes/(?P<recipe_id>\d+)/favorite',
#     basename='favorite',
#     viewset=FavoriteViewSet
#     )

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/token/login', login, name='login'),
    path('v1/auth/token/logout', logout, name='logout'),
    ]