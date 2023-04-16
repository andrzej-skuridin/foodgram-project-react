from django.urls import path, include
from rest_framework import routers

from api.views import (
    TagViewSet,
    IngredientViewSet,
    RecipeViewSet,
    FavoriteViewSet,
    SubscriptionViewSet,
    # SubscriptionAddDeleteViewSet,
)

router = routers.DefaultRouter()

router.register(
    prefix='tags',
    basename='tags',
    viewset=TagViewSet
)
router.register(
    prefix='ingredients',
    basename='ingredients',
    viewset=IngredientViewSet
)
router.register(
    prefix='recipes',
    basename='recipes',
    viewset=RecipeViewSet
)
router.register(
    prefix=r'recipes/(?P<recipe_id>\d+)/favorite',
    viewset=FavoriteViewSet,
    basename='favorite'
)
router.register(
    prefix=r'users/(?P<user_id>\d+)/subscribe',
    viewset=SubscriptionViewSet,
    basename='subscribe'
)
router.register(
    prefix=r'users/subscriptions',
    viewset=SubscriptionViewSet,
    basename='subscriptions'
)


urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    ]
