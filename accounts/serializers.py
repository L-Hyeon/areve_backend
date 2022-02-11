from rest_framework import serializers

from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('usernumber', 'email', 'name', 'nickname', 'birth', 'phonenumber', 'joindate', 'location')
        #exclude = ('rate', 'lastLogin', 'is_active', 'is_admin','postcode')

class OtherUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('usernumber', 'email', 'nickname', 'birth', 'rate', 'joindate', 'location')
        #exclude = ('name', 'phonenumber', 'lastLogin', 'is_active', 'is_admin', 'postcode')