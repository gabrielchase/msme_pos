from django.conf.urls import url, include

from menu_item.views import (
    MenuItemListAPIView,
    MenuItemCreateAPIView,
    MenuItemDetailAPIView
)


urlpatterns = [
    # Routes for MenuItem 
    url(r'(?P<full_business_name>[\w\-]+)/create/$', MenuItemCreateAPIView.as_view(), name='menu_items_create'),
    url(r'(?P<full_business_name>[\w\-]+)/(?P<menu_item_name>[\w\-]+)/$', MenuItemDetailAPIView.as_view(), name='menu_items_detail')
]
