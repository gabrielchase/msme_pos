from rest_framework import permissions


class GetAndUpdateOwnProfile(permissions.BasePermission):
    """ Allow users to edit their own profile """

    def has_object_permission(self, request, view, user_profile):
        """ Check if user is trying their update or delete their own profile """

        return user_profile.id == request.user.id or request.user.is_superuser


class GetAndUpdateOwnMenuItem(permissions.BasePermission):
    """ Allow user to update or delete their own menu item """

    def has_object_permission(self, request, view, menu_item):
        return menu_item.user_profile == request.user or request.user.is_superuser

class CreateOrderItem(permissions.BasePermission):
    """ Allow user to create an order of theor own menu item """

    def has_object_permission(self, request, view, instance):
        
        if instance.__class__.__name__ == 'MenuItem':
            return instance.user_profile == request.user
        elif instance.__class__.__name__ == 'ItemOrder':
            return instance.menu_item.user_profile == request.user or request.user.is_superuser


class GetAndUpdateOwnOrderItem(permissions.BasePermission):
    """ Allow user to update or delete their own menu item orders"""

    def has_object_permission(self, request, view, order):
        print(order)
        print(order.menu_item)
        return order.menu_item.user_profile == request.user or request.user.is_superuser