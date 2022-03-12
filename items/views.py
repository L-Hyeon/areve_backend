from rest_framework.views import APIView
from rest_framework.response import Response

from orders.models import Order
from orders.serializers import OrderSerializer
from .serializers import ItemSerializer, ItemSearchSerializer
from core.utils import loginDecorator
import json
from .models import Item
from django.db.models import Q

class Apply(APIView):
  @loginDecorator
  def post(self, request):
    data = json.loads(request.body)
    loc = data["location"] + ' ' + data["detailLoc"]
    images = data["images"]
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
      target = Item.objects.all().order_by('-like')[:4]
    elif (param == 1):
      target = Item.objects.all().order_by('-uploaded')[:4]
    else:
      q = request.user.like.split()
      if (len(q) == 0):
        return Response(status=404)
      target = []
      for e in q:
        target.append(Item.objects.get(itemnumber=e))
      if (len(target) < 4):
        return Response(ItemSearchSerializer(target, many=True).data)
      else:
        return Response(ItemSearchSerializer(target[:4], many=True).data)
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

class GetItemLiked(APIView):
  def get(self, request, pageNum):
    q = request.user.like.split()
    if (not q):
      return Response(status=404)
    target = []
    print(q)
    for e in q:
      target.append(Item.objects.get(itemnumber=e))
    target = target[12*pageNum : 12*(pageNum + 1)]
    if (len(target) == 0):
      return Response(status=404)
    return Response(ItemSearchSerializer(target, many=True).data)

class GetItemSimilar(APIView):
  def get(self, request, itemNum):
    original = Item.objects.get(itemnumber=itemNum)
    originalSigungu = original.sigungu
    originalCategory = original.category
    target = Item.objects.filter(Q(category=originalCategory) & Q(sigungu=originalSigungu))
    if (len(target) > 3):
      target = target[:3]
    return Response(ItemSearchSerializer(target, many=True).data)

class GetItemApplied(APIView):
  def get(self, request, pageNum, userNum = None):
    if (userNum):
      target = Item.objects.filter(writer = userNum)
    else:
      target = Item.objects.filter(writer = request.user.usernumber)
    
    target = target[12*pageNum : 12*(pageNum + 1)]
    if (len(target) == 0):
      return Response(status=404)
    if (len(target) == 1):
      return Response(ItemSearchSerializer(target).data)
    return Response(ItemSearchSerializer(target, many=True).data)

class GetItemOrdered(APIView):
  def get(self, request):
    user = request.user
    orders = Order.objects.filter(buyer = request.user.usernumber)
    if (not orders):
      return Response(status=404)
    target = []
    for e in orders:
      i = Item.objects.get(itemnumber = e.itemnumber)
      target.append((ItemSearchSerializer(i).data, OrderSerializer(e).data))
    return Response(target)

class Chk(APIView):
  def get(self, request):
    chk = Item.objects.all()
    #serializer = ItemSerializer(chk, many=True)
    #target = Item.objects.filter(Q(title__icontains="1"))
    #q2 = Item.objects.filter(title__icontains="3")
    #return Response(ItemSearchSerializer(target.union(q2), many=True).data)
    for e in chk:
      print(e.itemnumber)
    return Response(ItemSearchSerializer(chk, many=True).data)

