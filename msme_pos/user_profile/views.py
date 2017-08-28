from rest_framework import (
    viewsets,
    filters,
    status,
    mixins,
    generics
)

from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken

from rest_framework.permissions import (
    IsAdminUser,
    IsAuthenticated,
)

from user_profile.models import UserProfile

from user_profile.serializers import UserProfileSerializer

from user_profile.permissions import (
    GetAndUpdateOwnProfile,
    GetAndUpdateOwnMenuItem,
    GetOwnOrders,
    GetAndUpdateOwnOrderItem,
    CreateOrderItem
)


class UserProfileListAPIView(generics.ListAPIView):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminUser,)


class UserProfileCreateAPIView(generics.CreateAPIView):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()


class UserProfileDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """ Handles creating, updating, and deleting UserProfile """

    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    lookup_field = 'full_business_name'
    filter_backends = (filters.SearchFilter,)
    search_fields = (
        'email', 'business_name', 'identifier', 'full_business_name',
        'owner_surname', 'owner_given_name',
        'address', 'city', 'state'
    )
    authentication_classes = (TokenAuthentication,)
    permission_classes = (GetAndUpdateOwnProfile,)
    

class LoginViewSet(viewsets.ViewSet):
    """ Checks email and password and returns an authtoken """

    serializer_class = AuthTokenSerializer

    def create(self, request):
        """ Use the ObtainAuthToken APIView to validate and create a token """

        return ObtainAuthToken().post(request)
