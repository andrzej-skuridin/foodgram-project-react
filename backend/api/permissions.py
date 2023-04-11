from rest_framework import permissions


class AuthenticatedOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)


class RecipePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated
                    and (request.method == 'DELETE'
                         or obj.author == request.user)
                    )
                or (request.user.is_authenticated
                    and (request.method == 'PATCH'
                         or obj.author == request.user)
                    )
                )
