from rest_framework import viewsets
from rest_framework import filters
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import (
    IsAdminUser,
    IsAuthenticated,
)

from api.models import (
    UserProfile,
    MenuItem,
    ItemOrder,
)

from api.serializers import (
    UserProfileSerializer,
    MenuItemSerializer,
    ItemOrderSerializer,
)

from api.permissions import (
    GetAndUpdateOwnProfile,
    GetAndUpdateOwnMenuItem,
    GetAndUpdateOwnOrderItem
)


class UserProfileListAPIView(generics.ListAPIView):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminUser,)


class UserProfileCreateAPIView(generics.CreateAPIView):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()


class UserProfileDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """ Handles creating, updating, and deleting UserProfile """

    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    lookup_field = 'full_business_name'
    filter_backends = (filters.SearchFilter,)
    search_fields = (
        'email', 'business_name', 'identifier', 'full_business_name',
        'owner_surname', 'owner_given_name',
        'address', 'city', 'state'
    )
    authentication_classes = (TokenAuthentication,)
    permission_classes = (GetAndUpdateOwnProfile,)
    

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


class LoginViewSet(viewsets.ViewSet):
    """ Checks email and password and returns an authtoken """

    serializer_class = AuthTokenSerializer

    def create(self, request):
        """ Use the ObtainAuthToken APIView to validate and create a token """

        return ObtainAuthToken().post(request)


class ItemOrderCreateAPIView(generics.CreateAPIView):
    serializer_class = ItemOrderSerializer
    queryset = ItemOrder.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, full_business_name=None, menu_item_name=None):
        menu_item = MenuItem.objects.get(url_param_name=menu_item_name)
        serialized_menu_item = MenuItemSerializer(menu_item)

        return Response(serialized_menu_item.data)

    def post(self, request, full_business_name=None, menu_item_name=None, *args):
        menu_item = MenuItem.objects.get(url_param_name=menu_item_name)

        item_order = ItemOrder.objects.create(
            quantity=request.data.get('quantity'),
            additional_notes=request.data.get('additional_notes'),
            menu_item=menu_item
        )

        serialized_item_order = ItemOrderSerializer(item_order)

        return Response(serialized_item_order.data)


class ItemOrderDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """ Serializer for UserProfile objects"""
    
    serializer_class = ItemOrderSerializer
    queryset = ItemOrder.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (GetAndUpdateOwnOrderItem,)
    lookup_field = 'pk'
    lookup_url_kwarg = 'item_order_pk'