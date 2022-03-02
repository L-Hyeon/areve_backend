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
      pricePerHour = False if (data["pricePerHour"]=="false") else True,
      writer = request.user.usernumber,
      writerName=request.user.nickname,
      startDate=data["startDate"],
      endDate=data["endDate"]
    )
    return Response(item.itemnumber)

class GetItem(APIView):
  def get(self, request, itemnumber):
    target = Item.objects.get(itemnumber = itemnumber)
    return Response(ItemSerializer(target).data)

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
    
    if (len(target) == 1):
      return Response(ItemSearchSerializer(target).data)
    return Response(ItemSearchSerializer(target, many=True).data)

class GetItemWithCategory(APIView):
  def get(self, request, catNum, pageNum):
    target = Item.objects.filter(category=catNum)[12*pageNum : 12*(pageNum + 1)]
    if (len(target) == 0):
      return Response(status=404)
    if (len(target) == 1):
      return Response(ItemSearchSerializer(target).data)
    return Response(ItemSearchSerializer(target, many=True).data)

  def post(self, request, catNum, pageNum):
    # 조건을 가진 쿼리문 생성하기
    target = Item.objects.filter(category=catNum)[12*pageNum : 12*(pageNum + 1)]
    return Response()

class GetItemSearch(APIView):
  def get(self, request, pageNum):
    searchKey = request.GET.get('q')
    target = Item.objects.filter(Q(title__icontains=searchKey))

    lowerpriceKey = request.GET.get('lowerprice')
    higherpriceKey = request.GET.get('higherprice')
    if (lowerpriceKey and higherpriceKey):
      target = target.intersection(Item.objects.filter(Q(price__gte=lowerpriceKey) & Q(price__lte=higherpriceKey)))
    elif (lowerpriceKey):
      target = target.intersection(Item.objects.filter(price__gte=lowerpriceKey))
    elif (higherpriceKey):
      target = target.intersection(Item.objects.filter(price__lte=higherpriceKey))
    
    lowerdateKey = request.GET.get('lowerdate')
    higherdateKey = request.GET.get('higherdate')
    # 아이템 데이터에 가능한 일자 추가 후 작업예정

    locationKey = request.GET.get('location')
    if (locationKey): target = target.intersection(Item.objects.filter(location__icontains=locationKey))

    target = target[12*pageNum : 12*(pageNum + 1)]
    if (len(target) == 0):
      return Response(status=404)
    if (len(target) == 1):
      return Response(ItemSearchSerializer(target).data)
    return Response(ItemSearchSerializer(target, many=True).data)


class GetItemUserLiked(APIView):
  def get(self, request):
    q = request.user.like.split()
    if (not q):
      return Response(status=404)

    target = Item.objects.filter(itemnumber=q[0])
    if (len(target) == 1):
      return Response(ItemSearchSerializer(target).data)

    for x in q[1:]:
      target = target.union(Item.objects.filter(itemnumber=x))

    return Response(ItemSearchSerializer(target, many=True).data)

class Chk(APIView):
  def get(self, request):
    #chk = Item.objects.all()
    #serializer = ItemSerializer(chk, many=True)
    target = Item.objects.filter(Q(title__icontains="1"))
    q2 = Item.objects.filter(title__icontains="3")
    #target = Item.objects.filter(title__icontains="3")
    return Response(ItemSearchSerializer(target.union(q2), many=True).data)


