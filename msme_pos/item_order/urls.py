from django.conf.urls import url, include

from item_order.views import (
    ItemOrderListAPIView,
    ItemOrderCreateAPIView,
    ItemOrderDetailAPIView
)


urlpatterns = [
    url(r'(?P<full_business_name>[\w\-]+)/orders/$', ItemOrderListAPIView.as_view(), name='item_order_list'),
    url(r'(?P<full_business_name>[\w\-]+)/(?P<menu_item_name>[\w\-]+)/$', ItemOrderCreateAPIView.as_view(), name='item_order_create'),
    url(r'(?P<full_business_name>[\w\-]+)/(?P<menu_item_name>[\w\-]+)/(?P<item_order_pk>[\w\-]+)/$', ItemOrderDetailAPIView.as_view(), name='item_order_detail'),
]
