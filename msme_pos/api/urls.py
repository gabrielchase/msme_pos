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
    ItemOrderCreateAPIView,
    ItemOrderDetailAPIView
)

router = DefaultRouter()

# router.register('profile', UserProfileViewSet, 'profile')
# router.register('menu_items', MenuItemViewSet, 'menu_items')

# Set base_name if its not a ModelViewSet
router.register('login', LoginViewSet, base_name='login') 

urlpatterns = [
    url(r'', include(router.urls)),

    # Routes for UserProfile 
    url(r'profiles/$', UserProfileListAPIView.as_view(), name='profiles_list'),
    url(r'profiles/create/$', UserProfileCreateAPIView.as_view(), name='profiles_create'),
    url(r'profiles/(?P<full_business_name>[\w\-]+)/$', UserProfileDetailAPIView.as_view(), name='profiles_detail'),
    
    # Routes for MenuItem 
    url(r'profiles/(?P<full_business_name>[\w\-]+)/menu_item/create/$', MenuItemCreateAPIView.as_view(), name='menu_items_create'),
    url(r'profiles/(?P<full_business_name>[\w\-]+)/menu_item/(?P<menu_item_name>[\w\-]+)/$', MenuItemDetailAPIView.as_view(), name='menu_items_detail'),

    # Routes for ItemOrder 
    url(r'profiles/(?P<full_business_name>[\w\-]+)/menu_item/(?P<menu_item_name>[\w\-]+)/order/(?P<item_order_pk>[\w\-]+)/$', ItemOrderDetailAPIView.as_view(), name='item_order_detail'),
    url(r'profiles/(?P<full_business_name>[\w\-]+)/menu_item/(?P<menu_item_name>[\w\-]+)/order/$', ItemOrderCreateAPIView.as_view(), name='item_order_create'),
    
    # Route for al 
    url(r'menu_items/$', MenuItemListAPIView.as_view(), name='menu_items_list'),
    # url(r'menu_items/(?P<menu_item_pk>\d+)/$', MenuItemDetailAPIView.as_view(), name='menu_items_detail'),
    # url(r'menu_items/(?P<menu_item_pk>\d+)/item_order/create/$', ItemOrderCreateAPIView.as_view(), name='item_order_create'),
]
