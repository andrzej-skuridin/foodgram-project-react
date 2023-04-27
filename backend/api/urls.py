from django.urls import include, path
from rest_framework import routers

from api.views import (
    FavoriteViewSet,
    IngredientViewSet,
    MeViewSet,
    RecipeViewSet,
    ShoppingCartViewSet,
    SubscriptionViewSet,
    TagViewSet,
)

router = routers.DefaultRouter()

router.register(prefix='tags', basename='tags', viewset=TagViewSet)
router.register(
    prefix='ingredients', basename='ingredients', viewset=IngredientViewSet
)
router.register(prefix='recipes', basename='recipes', viewset=RecipeViewSet)
router.register(
    prefix=r'recipes/(?P<recipe_id>\d+)/favorite',
    viewset=FavoriteViewSet,
    basename='favorite',
)
router.register(
    prefix=r'users/(?P<user_id>\d+)/subscribe',
    viewset=SubscriptionViewSet,
    basename='subscribe',
)
router.register(
    prefix=r'users/subscriptions',
    viewset=SubscriptionViewSet,
    basename='subscriptions',
)
router.register(
    prefix=r'recipes/(?P<recipe_id>\d+)/shopping_cart',
    viewset=ShoppingCartViewSet,
    basename='shopping_cart',
)
router.register(prefix=r'users/me', viewset=MeViewSet, basename='me')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
