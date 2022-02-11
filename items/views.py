from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ItemSerializer
from core.utils import loginDecorator
import json
from .models import Item

class Apply(APIView):
  @loginDecorator
  def post(self, request):
    data = json.loads(request.body.decode('utf-8'))
    loc = data["location"] + ' ' + data["detailLoc"]
    item = Item.objects.create_item(
      title = data["title"],
      category = data["category"],
      content = data["content"],
      postcode = data["postcode"],
      location = loc,
      cntImg = data["cntImg"],
      images = data["images"],
      price = data["price"],
      pricePerHour = data["pricePerHour"],
      writer = request.user.usernumber
    )
    return Response("Item Applied")

class GetItem(APIView):
  def get(self, request, param):
    target = Item.objects.filter(itemnumber = param)
    return Response(ItemSerializer(target, many=True).data)

class GetItemWithCategory(APIView):
  def get(self, request, param):
    return Response(ItemSerializer(Item.objects.filter(category=param), many=True).data)

class Chk(APIView):
  def get(self, request):
    chk = Item.objects.all()
    serializer = ItemSerializer(chk, many=True)
    return Response(serializer.data)