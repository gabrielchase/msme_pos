from django.shortcuts import render

from rest_framework import viewsets
from rest_framework import filters
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken

from api.models import UserProfile
from api.serializers import UserProfileSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    """ Handles creating, updating, and deleting UserProfile """

    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = (
        'email', 'business_name', 'identifier', 
        'owner_surname', 'owner_given_name',
        'address', 'city', 'state'
    )
    

class LoginViewSet(viewsets.ViewSet):
    """ Checks email and password and returns an authtoken """

    serializer_class = AuthTokenSerializer

    def create(self, request):
        """ Use the ObtainAuthToken APIView to validate and create a token """

        return ObtainAuthToken().post(request)
