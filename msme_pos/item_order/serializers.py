from rest_framework import (
    serializers,
    pagination
)

from item_order.models import ItemOrder


class ItemOrderSerializer(serializers.ModelSerializer):
    """ Serializer for an User's Menu Item order """

    # menu_item = MenuItemSerializer(read_only=True)

    class Meta:
        model = ItemOrder
        fields = ('id', 'quantity', 'menu_item', 'ordered_on', 'additional_notes')
        extra_kwargs = {
            'menu_item': {'read_only': True},
        }

