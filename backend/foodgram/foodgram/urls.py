from django.contrib import admin
from django.urls import include
from django.urls import path

urlpatterns = [
    path('', include('users.urls', namespace='users')),
    path('admin/', admin.site.urls),
    ]
