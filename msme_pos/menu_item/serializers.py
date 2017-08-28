from rest_framework import (
    serializers,
    pagination
)

from menu_item.models import MenuItem


class MenuItemSerializer(serializers.ModelSerializer):
    """ Serializer for user's menu item """

    item_orders = serializers.SerializerMethodField('paginated_item_orders')

    class Meta: 
        model = MenuItem
        fields = ('id', 'name', 'url_param_name', 'description', 'price', 'added_on', 'user_profile', 'item_orders')
        extra_kwargs = {
            'url_param_name': {'read_only': True},
            'user_profile': {'read_only': True}
        }

    def paginated_item_orders(self, menu_item):
        request = self.context.get('request')
        item_orders = ItemOrder.objects.filter(menu_item=menu_item).order_by('-ordered_on')
        
        if request:     
            """ In Get ItemOrderDetail view """

            date_query = request.query_params.get('date')

            if date_query:
                datetime_date_query = pytz.utc.localize(datetime.datetime.strptime(date_query, '%Y-%m-%d'))
                item_orders = item_orders.filter(ordered_on__date=datetime_date_query)
            
            paginator = pagination.PageNumberPagination()
            page = paginator.paginate_queryset(item_orders, self.context['request'])
            serializer = ItemOrderSerializer(page, many=True, context={'request': self.context['request']})
            
            return serializer.data
        else: 
            """ In Create ItemOrderDetail view so just return 
            number of orders """

            return len(item_orders)
        
