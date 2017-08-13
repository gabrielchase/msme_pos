from django.shortcuts import render

from rest_framework import viewsets
from rest_framework import filters
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken

from api.models import (
    UserProfile,
    MenuItem   
)

from api.serializers import (
    UserProfileSerializer,
    MenuItemSerializer    
)

from api.permissions import (
    UpdateOwnProfile,
    PostOwnMenuItem,
    GetOwnMenu
)


class UserProfileViewSet(viewsets.ModelViewSet):
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
    permission_classes = (UpdateOwnProfile,)

    
    @detail_route(methods=['get'], permission_classes=[GetOwnMenu], url_path='menu')
    def menu(self, request, full_business_name=None):

        if full_business_name != str(request.user):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        context = {
            'request': request
        }

        menu_items = MenuItem.objects.filter(user_profile=request.user)
        menu_item_serializer = MenuItemSerializer(menu_items, many=True, context=context)
        
        return Response(menu_item_serializer.data)


class MenuItemViewSet(viewsets.ModelViewSet):
    """ Handles creating, updating, and deleting UserProfile's MenuItem """

    serializer_class = MenuItemSerializer
    queryset = MenuItem.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (PostOwnMenuItem,)

    def perform_create(self, serializer):
        """ Set current user as the MenuItem's user_profile """

        serializer.save(user_profile=self.request.user)


class LoginViewSet(viewsets.ViewSet):
    """ Checks email and password and returns an authtoken """

    serializer_class = AuthTokenSerializer

    def create(self, request):
        """ Use the ObtainAuthToken APIView to validate and create a token """

        return ObtainAuthToken().post(request)
