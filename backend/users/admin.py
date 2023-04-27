from django.contrib import admin

from .models import User, Subscription


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'username',)
    search_fields = ('id', 'email', 'username',)
    list_filter = ('id', 'email', 'username',)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'follower',)
    search_fields = ('id', 'author', 'follower',)
    list_filter = ('id', 'author', 'follower',)
