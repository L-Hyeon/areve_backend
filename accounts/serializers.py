from rest_framework import serializers

from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('usernumber', 'email', 'name', 'nickname', 'birth', 'phonenumber', 'joindate', 'location', 'rate', 'location', 'postcode', 'sigungu', 'numWrittenReview', 'numItemSharing')
''
class OtherUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('usernumber', 'email', 'nickname', 'birth', 'rate', 'joindate', 'location', 'numItemSharing')