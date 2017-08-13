from rest_framework import permissions


class UpdateOwnProfile(permissions.BasePermission):
    """ Allow users to edit their own profile """

    def has_object_permission(self, request, view, obj):
        """ Check if user is trying their update or delete their own profile """

        if request.method in permissions.SAFE_METHODS: 
            return True

        return obj.id == request.user.id

class GetOwnMenu(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        """ Check if user is getting their own menu """

        return obj.full_business_name == str(request.user)


class PostOwnMenuItem(permissions.BasePermission):
    """ Allow user to update their own menu item """

    def has_object_permission(self, request, view, obj):
        print(obj.user_profile)
        print(request.user)
        return obj.user_profile == request.user
