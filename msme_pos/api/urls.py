from django.conf.urls import url, include

from rest_framework.routers import DefaultRouter

from api.views import (
    UserProfileViewSet,
    LoginViewSet,
    MenuItemListAPIView,
    MenuItemCreateAPIView,
    MenuItemDetailAPIView
)

router = DefaultRouter()

router.register('profile', UserProfileViewSet, 'profile')
# router.register('menu_items', MenuItemViewSet, 'menu_items')

# Set base_name if its not a ModelViewSet
router.register('login', LoginViewSet, base_name='login') 

urlpatterns = [
    url(r'', include(router.urls)),
    url(r'menu_items/$', MenuItemListAPIView.as_view(), name='menu_items_list'),
    url(r'menu_items/create/$', MenuItemCreateAPIView.as_view(), name='menu_items_create'),
    url(r'menu_items/(?P<pk>\d+)/$', MenuItemDetailAPIView.as_view(), name='menu_items_detail')
]
