from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken import views

from api.views import TagViewSet, UserViewSet, IngredientViewSet, logout

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
    path('auth/token/login', views.obtain_auth_token, name='login'),
    # path('auth/token/logout', logout, name='logout'),
    ]
