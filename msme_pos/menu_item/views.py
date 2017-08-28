from rest_framework import (
    viewsets,
    filters,
    status,
    mixins,
    generics
)

from rest_framework.permissions import (
    IsAdminUser,
    IsAuthenticated,
)

from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication

from menu_item.models import MenuItem
from menu_item.serializers import MenuItemSerializer

from user_profile.permissions import GetAndUpdateOwnMenuItem


class MenuItemListAPIView(generics.ListAPIView):
    serializer_class = MenuItemSerializer
    queryset = MenuItem.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminUser,)


class MenuItemCreateAPIView(generics.CreateAPIView):
    serializer_class = MenuItemSerializer
    queryset = MenuItem.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        new_menu_item = MenuItem.objects.create(
            name=request.data.get('name'),
            description=request.data.get('description'),
            price=request.data.get('price'),
            user_profile=request.user
        )

        serialized_menu_item = MenuItemSerializer(new_menu_item)

        return Response(serialized_menu_item.data)


class MenuItemDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """ Handles getting, updating, and deleting UserProfile's MenuItem """

    serializer_class = MenuItemSerializer
    queryset = MenuItem.objects.all()
    lookup_field = 'url_param_name'
    lookup_url_kwarg = 'menu_item_name'
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, GetAndUpdateOwnMenuItem,)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
