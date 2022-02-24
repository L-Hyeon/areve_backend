from rest_framework import serializers

from .models import Item

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

class ItemSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('itemnumber', 'category', 'title', 'cntImg', 'image1', 'image2', 'image3', 'image4', 'image5', 'image6', 'image7', 'image8', 'location', 'sigungu', 'price', 'pricePerHour', 'rate', 'reviews', 'like')

class ItemReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('itemnumber', 'title', 'image1')