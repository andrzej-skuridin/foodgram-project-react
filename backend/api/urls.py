from django.urls import path, include
from rest_framework import routers

from api.views import (
    TagViewSet,
    IngredientViewSet,
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

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    ]
