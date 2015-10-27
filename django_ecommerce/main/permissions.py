from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # allow all read type request
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True

        # this leaves us with write request (i.e. POST / PUT / DELETE)
        return obj.user == request.user
