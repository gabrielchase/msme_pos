from rest_framework import serializers

from api.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    """ Serializer for UserProfile objects"""

    class Meta:
        model = UserProfile
        fields = (
            'id', 'email', 'business_name', 'identifier', 'full_business_name',
            'owner_surname', 'owner_given_name', 'password',
            'address', 'city', 'state'
        )
        read_only_fields = ('full_business_name',)
        extra_kwargs = {'password': { 'write_only': True }}

    def create(self, validated_data):
        """ Create and return a new user """

        user = UserProfile(
            email=validated_data.get('email'),
            business_name=validated_data.get('business_name'),
            identifier=validated_data.get('identifier'),
            owner_surname=validated_data.get('owner_surname'),
            owner_given_name=validated_data.get('owner_given_name'),
            address=validated_data.get('address'),
            city=validated_data.get('city'),
            state=validated_data.get('state')
        )

        user.full_business_name = user.get_full_name()

        user.set_password(validated_data.get('password'))
        user.save()

        return user

    def update(self, full_business_name, validated_data):
        user = UserProfile.objects.get(full_business_name=full_business_name)

        for k, v in validated_data.items():
            setattr(user, k, v)
        
        user.full_business_name = user.get_full_name()
        user.save()

        return user
