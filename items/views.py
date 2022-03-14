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

class ModifyItem(APIView):
  @loginDecorator
  def post(self, request, itemNum):
    item = Item.objects.get(itemnumber=itemNum)
    if (request.user.usernumber != item.writer):
      return Response(status=400)
    item.delete()
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
    Response(item.itemnumber)

class DeleteItem(APIView):
  @loginDecorator
  def get(self, request, itemNum):
    user = request.user
    item = Item.objects.get(itemnumber=itemNum)
    if (item.writer != user.usernumber):
      return Response(status=400)
    item.delete()
    return Response(status=200)

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
      target = []
      for e in q:
        target.append(Item.objects.get(itemnumber=e))
        if (len(target) == 2):
          break
      return Response(ItemSearchSerializer(target, many=True).data)
    if (len(target) == 1):
      return Response(ItemSearchSerializer(target).data)
    return Response(ItemSearchSerializer(target, many=True).data)

class GetItemSearch(APIView):
  def get(self, request, pageNum):
    searchKey = request.GET.get('q')
    category = request.GET.get('category')
    seller = request.GET.get('seller')
    if (seller == "-1"): seller = request.user.usernumber
    location = request.GET.get('location')
    start = request.GET.get('start')
    end = request.GET.get('end')
    lower = request.GET.get('lower')
    upper = request.GET.get('upper')
    order = request.GET.get('order')

    if (searchKey):
      target = Item.objects.filter(Q(title__icontains=searchKey))
    if (category):
      target = Item.objects.filter(category=int(category))
    if (seller):
      target = Item.objects.filter(writer=int(seller))
    
    if (lower and upper):
      lower = int(lower)
      upper = int(upper)
      target = target.intersection(Item.objects.filter(Q(price__gte=lower) & Q(price__lte=upper)))
    elif (lower):
      lower = int(lower)
      target = target.intersection(Item.objects.filter(price__gte=lower))
    elif (upper):
      upper = int(upper)
      target = target.intersection(Item.objects.filter(price__lte=upper))
    
    if (start and end):
      start = start.replace('.', '').replace(' ', '-')
      end = end.replace('.', '').replace(' ', '-')
      target = target.intersection(Item.objects.filter(Q(startDate__lte=start) & Q(endDate__gte=end)))
    elif (start):
      start = start.replace('.', '').replace(' ', '-')
      target = target.intersection(Item.objects.filter(Q(startDate__gte=start) | Q(endDate__gte=start)))
    elif (end):
      end = end.replace('.', '').replace(' ', '-')
      target = target.intersection(Item.objects.filter(Q(startDate__lte=end) | Q(endDate__gte=end)))
    
    if (location):
      target = target.intersection(Item.objects.filter(location__icontains=location))

    if (order == "0"):
      target = target.order_by('-like')[12*pageNum : 12*(pageNum + 1)]
    else:
      target = target.order_by('-uploaded')[12*pageNum : 12*(pageNum + 1)]
    if (len(target) == 0):
      return Response(status=404)
    return Response(ItemSearchSerializer(target, many=True).data)

class GetItemLiked(APIView):
  def get(self, request, pageNum):
    location = request.GET.get('location')
    start = request.GET.get('start')
    end = request.GET.get('end')
    lower = request.GET.get('lower')
    upper = request.GET.get('upper')
    order = request.GET.get('order')

    q = request.user.like.split()
    if (not q):
      return Response(status=404)

    target = Item.objects.filter(itemnumber=q[0])
    if (len(q) > 1):
      for e in q[1:]:
        target = target.union(Item.objects.filter(itemnumber=e))
    
    if (lower and upper):
      lower = int(lower)
      upper = int(upper)
      target = target.intersection(Item.objects.filter(Q(price__gte=lower) & Q(price__lte=upper)))
    elif (lower):
      lower = int(lower)
      target = target.intersection(Item.objects.filter(price__gte=lower))
    elif (upper):
      upper = int(upper)
      target = target.intersection(Item.objects.filter(price__lte=upper))
    
    if (start and end):
      start = start.replace('.', '').replace(' ', '-')
      end = end.replace('.', '').replace(' ', '-')
      target = target.intersection(Item.objects.filter(Q(startDate__lte=start) & Q(endDate__gte=end)))
    elif (start):
      start = start.replace('.', '').replace(' ', '-')
      target = target.intersection(Item.objects.filter(Q(startDate__gte=start) | Q(endDate__gte=start)))
    elif (end):
      end = end.replace('.', '').replace(' ', '-')
      target = target.intersection(Item.objects.filter(Q(startDate__lte=end) | Q(endDate__gte=end)))
    
    if (location):
      target = target.intersection(Item.objects.filter(location__icontains=location))

    if (order == "0"):
      target = target.order_by('-like')[12*pageNum : 12*(pageNum + 1)]
    else:
      target = target.order_by('-uploaded')[12*pageNum : 12*(pageNum + 1)]

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
    #chk = Item.objects.all()
    #serializer = ItemSerializer(chk, many=True)
    #target = Item.objects.filter(Q(title__icontains="1"))
    #q2 = Item.objects.filter(title__icontains="3")
    #return Response(ItemSearchSerializer(target.union(q2), many=True).data)
    chk = Item.objects.filter(itemnumber=0)
    t = Item.objects.filter(itemnumber = 4)
    chk = chk.union(t)
    print(chk, t)
    return Response(ItemSearchSerializer(chk, many=True).data)

