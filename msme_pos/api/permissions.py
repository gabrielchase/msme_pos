from rest_framework import permissions


class GetAndUpdateOwnProfile(permissions.BasePermission):
    """ Allow users to edit their own profile """

    def has_object_permission(self, request, view, obj):
        """ Check if user is trying their update or delete their own profile """

        return obj.id == request.user.id


class GetAndUpdateOwnMenuItem(permissions.BasePermission):
    """ Allow user to update or delete their own menu item """

    def has_object_permission(self, request, view, obj):
        return obj.user_profile == request.user or request.user.is_superuser
