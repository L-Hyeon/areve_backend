from unicodedata import category
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ItemSerializer, ItemSearchSerializer
from core.utils import loginDecorator
import json
from .models import Item

class Apply(APIView):
  #@loginDecorator
  def post(self, request):
    data = json.loads(request.body)
    loc = data["location"] + ' ' + data["detailLoc"]
    images = data["images"]
    print(request.user)
    for i in range(data["cntImg"], 9):
      images.append('')
    item = Item.objects.create_item(
      title = data["title"],
      category = data["category"],
      content = data["content"],
      postcode = data["postcode"],
      location = loc,
      sigungu = data["sigungu"],
      cntImg = data["cntImg"],
      images = images,
      price = data["price"],
      pricePerHour = data["pricePerHour"],
      writer = request.user.usernumber
    )
    return Response(item.itemnumber)

class GetItem(APIView):
  def get(self, request, itemnumber):
    target = Item.objects.get(itemnumber = itemnumber)
    return Response(ItemSerializer(target, many=True).data)

class GetItemWithCategory(APIView):
  def get(self, request, catNum, pageNum):
    target = Item.objects.filter(category=catNum)[12*pageNum : 12*(pageNum + 1)]
    if (len(target) == 0):
      return Response(status=404)
    return Response(ItemSearchSerializer(target, many=True).data)

  def post(self, request, catNum, pageNum):
    # 조건을 가진 쿼리문 생성하기
    target = Item.objects.filter(category=catNum)[12*pageNum : 12*(pageNum + 1)]
    return Response()

class GetItemInMain(APIView):
  def get(self, request, param):
    if (param == 0):
      target = Item.objects.all().order_by('-like')[:2]
    elif (param == 1):
      target = Item.objects.all().order_by('-uploaded')[:2]
    else:
      #좋아요 추가 후
      #target = Item.objects.filter(likedUser=request.user.usernumber)[:2]
      target = Item.objects.filter(title__icontains="이미지").order_by('-price')[:2]
    return Response(ItemSearchSerializer(target, many=True).data)

class Chk(APIView):
  def get(self, request):
    chk = Item.objects.all()
    serializer = ItemSerializer(chk, many=True)
    return Response(serializer.data)