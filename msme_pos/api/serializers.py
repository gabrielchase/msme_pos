from rest_framework import serializers

from api.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    """ Serializer for UserProfile objects"""

    class Meta:
        model = UserProfile
        fields = (
            'id', 'email', 'business_name', 'identifier', 
            'surname', 'given_name', 'password',
            'address', 'city', 'state'
        )
        extra_kwargs = {'password': { 'write_only': True }}

    def create(self, validated_data):
        """ Create and return a new user """

        user = UserProfile(
            email=validated_data.get('email'),
            business_name=validated_data.get('business_name'),
            identifier=validated_data.get('identifier'),
            surname=validated_data.get('surname'),
            given_name=validated_data.get('given_name'),
            address=validated_data.get('address'),
            city=validated_data.get('city'),
            state=validated_data.get('state')
        )

        user.set_password(validated_data.get('password'))
        user.save()

        return user
