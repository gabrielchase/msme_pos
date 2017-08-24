from rest_framework import (
    serializers,
    pagination
)

from api.models import (
    UserProfile,
    MenuItem,
    ItemOrder
)

import datetime
import pytz


class ItemOrderSerializer(serializers.ModelSerializer):
    """ Serializer for an User's Menu Item order """

    class Meta:
        model = ItemOrder
        fields = ('id', 'quantity', 'menu_item', 'ordered_on', 'additional_notes')
        extra_kwargs = {
            'menu_item': {'read_only': True},
        }


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
        

class UserProfileSerializer(serializers.ModelSerializer):
    """ Serializer for UserProfile objects"""
    
    menu_items = MenuItemSerializer(many=True, read_only=True)

    class Meta:
        model = UserProfile
        fields = (
            'id', 'email', 'business_name', 'identifier', 'full_business_name',
            'owner_surname', 'owner_given_name', 'password',
            'address', 'city', 'state', 'menu_items'
        )
        extra_kwargs = {
            'full_business_name': {'read_only': True},
            'password': { 'write_only': True }
        }

    def create(self, validated_data):
        """ Create and return a new user """

        user = UserProfile(
            email=validated_data.get('email'),
            business_name=validated_data.get('business_name'),
            identifier=validated_data.get('identifier'),
            owner_surname=validated_data.get('owner_surname'),
            owner_given_name=validated_data.get('owner_given_name'),
            address=validated_data.get('address'),
            city=validated_data.get('city'),
            state=validated_data.get('state')
        )

        user.full_business_name = user.get_full_name()

        user.set_password(validated_data.get('password'))
        user.save()

        return user

    def update(self, full_business_name, validated_data):
        user = UserProfile.objects.get(full_business_name=full_business_name)

        for k, v in validated_data.items():
            if k != 'password':
                setattr(user, k, v)
            else:
                user.set_password(validated_data.get('password'))
        
        user.full_business_name = user.get_full_name()
        user.save()

        return user
