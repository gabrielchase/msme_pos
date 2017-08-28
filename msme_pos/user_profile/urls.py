from django.conf.urls import url, include

from rest_framework.routers import DefaultRouter

from user_profile.views import (
    LoginViewSet,
    UserProfileListAPIView,
    UserProfileCreateAPIView,
    UserProfileDetailAPIView
)

router = DefaultRouter()

# router.register('profile', UserProfileViewSet, 'profile')
# router.register('menu_items', MenuItemViewSet, 'menu_items')

# Set base_name if its not a ModelViewSet
router.register('login', LoginViewSet, base_name='login') 

urlpatterns = [
    url(r'', include(router.urls)),

    url(r'$', UserProfileListAPIView.as_view(), name='profiles_list'),
    url(r'create/$', UserProfileCreateAPIView.as_view(), name='profiles_create'),
    url(r'(?P<full_business_name>[\w\-]+)/$', UserProfileDetailAPIView.as_view(), name='profiles_detail'),
]
