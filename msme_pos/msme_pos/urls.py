from django.conf.urls import url, include
from django.contrib import admin


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/profiles', include('user_profile.urls', namespace='profiles')),
    url(r'^api/menu_items', include('menu_item.urls', namespace='menu_items')),
    url(r'^api/item_orders', include('item_order.urls', namespace='item_orders'))
]
