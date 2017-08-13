from django.conf.urls import url, include

from rest_framework.routers import DefaultRouter

from api.views import (
    UserProfileViewSet,
    MenuItemViewSet,
    LoginViewSet
)

router = DefaultRouter()

router.register('profile', UserProfileViewSet, 'profile')
router.register('menu_items', MenuItemViewSet, 'menu_items')

# Set base_name if its not a ModelViewSet
router.register('login', LoginViewSet, base_name='login') 

urlpatterns = [
    url(r'', include(router.urls))
]
