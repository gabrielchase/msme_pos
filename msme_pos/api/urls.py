from django.conf.urls import url, include

from rest_framework.routers import DefaultRouter

from api.views import (
    LoginViewSet,
    UserProfileListAPIView,
    UserProfileCreateAPIView,
    UserProfileDetailAPIView,
    MenuItemListAPIView,
    MenuItemCreateAPIView,
    MenuItemDetailAPIView,
    ItemOrderCreateAPIView
)

router = DefaultRouter()

# router.register('profile', UserProfileViewSet, 'profile')
# router.register('menu_items', MenuItemViewSet, 'menu_items')

# Set base_name if its not a ModelViewSet
router.register('login', LoginViewSet, base_name='login') 

urlpatterns = [
    url(r'', include(router.urls)),
    url(r'profiles/$', UserProfileListAPIView.as_view(), name='profiles_list'),
    url(r'profiles/create/$', UserProfileCreateAPIView.as_view(), name='profiles_create'),
    url(r'profiles/(?P<full_business_name>[\w\-]+)/$', UserProfileDetailAPIView.as_view(), name='profiles_detail'),
    url(r'profiles/(?P<full_business_name>[\w\-]+)/menu_item/(?P<pk>\d+)/$', MenuItemDetailAPIView.as_view(), name='menu_items_detail'),
    url(r'profiles/(?P<full_business_name>[\w\-]+)/menu_item/create/$', MenuItemCreateAPIView.as_view(), name='menu_items_create'),
    url(r'menu_items/$', MenuItemListAPIView.as_view(), name='menu_items_list'),
    # url(r'menu_items/(?P<pk>\d+)/$', MenuItemDetailAPIView.as_view(), name='menu_items_detail'),
    # url(r'menu_items/(?P<pk>\d+)/item_order/create/$', ItemOrderCreateAPIView.as_view(), name='item_order_create'),
]
