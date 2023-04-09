from django.urls import path, include
from rest_framework import routers

from api.views import TagViewSet, UserViewSet, IngredientViewSet

router = routers.DefaultRouter()

router.register(
    prefix='tags',
    basename='tags',
    viewset=TagViewSet
)
router.register(
    prefix='users',
    viewset=UserViewSet,
    basename='users'
)
router.register(
    prefix='ingredients',
    basename='ingredients',
    viewset=IngredientViewSet
)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    # path('auth/token/login', login, name='login'),
    # path('auth/token/logout', logout, name='logout'),
    ]