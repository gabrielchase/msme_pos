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

from item_order.models import ItemOrder
from item_order.serializers import ItemOrderSerializer

from user_profile.permissions import (
    GetOwnOrders,
    GetAndUpdateOwnOrderItem,
    CreateOrderItem
)


class ItemOrderListAPIView(generics.RetrieveUpdateDestroyAPIView):
    """ View for a UserProfile to see all their orders """

    serializer_class = ItemOrderSerializer
    queryset = ItemOrder.objects.all()
    lookup_field = 'full_business_name'
    authentication_classes = (TokenAuthentication,)
    permission_classes = (GetOwnOrders,)

    def get(self, request, full_business_name):
        all_orders = ItemOrder.objects.all().filter(menu_item__user_profile=request.user)
        serialized_orders = ItemOrderSerializer(all_orders, many=True)
        # print(serialized_orders)
        return Response(serialized_orders.data)



class ItemOrderCreateAPIView(generics.CreateAPIView):
    serializer_class = ItemOrderSerializer
    queryset = ItemOrder.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (CreateOrderItem,)

    def get(self, request, full_business_name=None, menu_item_name=None):
        menu_item = MenuItem.objects.get(url_param_name=menu_item_name)

        if request.user == menu_item.user_profile:
            serialized_menu_item = MenuItemSerializer(menu_item)
            return Response(serialized_menu_item.data)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

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

