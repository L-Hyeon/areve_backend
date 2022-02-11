from django.shortcuts import render
from rest_framework.response import Response
from .models import Item
from rest_framework.views import APIView
from .serializers import ItemSerializer

class ProductListAPI(APIView):
    def get(self, request):
        queryset = Item.objects.all()
        print(queryset)
        serializer = ItemSerializer(queryset, many=True)
        return Response(serializer.data)