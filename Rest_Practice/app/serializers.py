from rest_framework import serializers

from app.models import User, Address


class AddressSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Address
        fields = ('url', 'id', 'a_address', 'a_user')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    address_set = AddressSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('url', 'id', 'u_name', 'u_password', 'address_set')
