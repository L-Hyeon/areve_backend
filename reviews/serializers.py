from attr import field
from rest_framework import serializers

from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class ReviewOverviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('score', 'reviewnumber', 'content')

class ReviewForItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('score', 'reviewnumber', 'content', 'writerName', 'numWriter')