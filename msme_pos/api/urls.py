from django.conf.urls import url, include

from rest_framework.routers import DefaultRouter

from api.views import (
    UserProfileViewSet
)

router = DefaultRouter()

router.register('profile', UserProfileViewSet)

urlpatterns = [
    url(r'', include(router.urls))
]