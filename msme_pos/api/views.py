from rest_framework import viewsets
from rest_framework import filters
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated


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
        serialized_menu_items = MenuItemSerializer(menu_items, many=True, context=context)
        
        return Response(serialized_menu_items.data)


class MenuItemCreateAPIView(generics.CreateAPIView):
    serializer_class = MenuItemSerializer
    queryset = MenuItem.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        new_menu_item = MenuItem.objects.create(
            name=request.data.get('name'),
            description=request.data.get('description'),
            price=request.data.get('price'),
            user_profile=request.user
        )

        serialized_menu_item = MenuItemSerializer(new_menu_item)

        return Response(serialized_menu_item.data)


class MenuItemDetailAPIView(mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.RetrieveAPIView):
    """ Handles getting, updating, and deleting UserProfile's MenuItem """

    serializer_class = MenuItemSerializer
    queryset = MenuItem.objects.all()
    lookup_field = 'pk'
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, PostOwnMenuItem,)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class LoginViewSet(viewsets.ViewSet):
    """ Checks email and password and returns an authtoken """

    serializer_class = AuthTokenSerializer

    def create(self, request):
        """ Use the ObtainAuthToken APIView to validate and create a token """

        return ObtainAuthToken().post(request)
