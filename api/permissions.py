from rest_framework import permissions
from .models import Follow


class IsOwnerOrFollowerReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # permissons for readonly
        if request.method in permissions.SAFE_METHODS:
            # not a private account -> anyone can read
            if not obj.profile.private:
                return True
            # if a private account -> followers can read
            elif request.user.is_authenticated and Follow.objects.filter(profile=request.user,
                                                                         followed=obj.profile).exist():
                return True
            # private account and unauthenticated/non-following users can't read
            else:
                return False

        return obj.profile == request.user


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.profile == request.user
