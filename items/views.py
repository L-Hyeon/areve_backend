from unicodedata import category
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ItemSerializer, ItemSearchSerializer
from core.utils import loginDecorator
import json
from .models import Item
from django.db.models import Q

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
      q = request.user.like.split()
      if (len(q) == 0):
        return Response(status=404)
      if (len(q) == 1):
        target = Item.objects.get(itemnumber=q[0])
        return Response(ItemSearchSerializer(target).data)
      else:
        target = Item.objects.filter(Q(itemnumber=q[0]) | Q(itemnumber=q[1]))
    return Response(ItemSearchSerializer(target, many=True).data)

class GetItemUserLiked(APIView):
  def get(self, request):
    q = request.user.like.split()
    target = Item.objects.filter(itemnumber=q[0])
    for x in q[1:]:
      target = target.union(Item.objects.filter(itemnumber=x))
    return Response(ItemSearchSerializer(target, many=True).data)

class Chk(APIView):
  def get(self, request):
    chk = Item.objects.all()
    serializer = ItemSerializer(chk, many=True)
    return Response(serializer.data)


#target = Item.objects.filter(title__icontains="이미지").order_by('-price')[:2]