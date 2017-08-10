from django.shortcuts import render

from rest_framework import viewsets

from api.models import UserProfile
from api.serializers import UserProfileSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    """ Handles creating, updating, and deleting UserProfile"""

    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    