from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ReviewForItemSerializer, ReviewOverviewSerializer, ReviewSerializer
from core.utils import loginDecorator
import json
from .models import Review
from items.models import Item
from items.serializers import ItemReviewSerializer
from orders.models import Order
from accounts.models import User

class WriteReview(APIView):
  @loginDecorator
  def post(self, request):
    data = json.loads(request.body)
    images = data["images"]
    for i in range(data["cntImg"], 6):
      images.append('')
    review = Review.objects.create_review(
      score = data["score"],
      content = data["content"],
      cntImg = data["cntImg"],
      images = images,
      numItem = data["itemnumber"],
      numWriter = request.user.usernumber,
      nameWriter = request.user.name,
      numOrder = data["ordernumber"]
    )
    order = Order.objects.get(ordernumber=data["ordernumber"])
    if (order): print(1)
    order.reviewWritten = True
    order.save()
    user = request.user
    user.numWrittenReview += 1
    user.save()

    item = Item.objects.get(itemnumber=data["itemnumber"])
    user = User.objects.get(usernumber=item.writer)
    cnt = 0
    for i in Item.objects.filter(writer=user.usernumber):
      cnt += i.reviews
    preRate = user.rate*cnt
    user.rate = (preRate + data["score"])/(cnt + 1)
    user.save()
    item.reviews += 1
    item.save()
    return Response(review.reviewnumber)

class GetReview(APIView):
  def get(self, request, reviewNum):
    target = Review.objects.get(reviewnumber = reviewNum)
    item = Item.objects.get(itemnumber=target.numItem)
    ret = [ReviewSerializer(target).data, ItemReviewSerializer(item).data]
    return Response(ret)

class GetReviewUserNumber(APIView):
  def get(self, request, userNum):
    user = User.objects.get(usernumber=userNum)
    applied = Item.objects.filter(writer=user.usernumber)
    reviews = []
    for e in applied:
      for r in Review.objects.filter(numItem=e.itemnumber):
        reviews.append(r)
    if (not reviews):
      return Response({})
    return Response(ReviewOverviewSerializer(reviews, many=True).data)

class GetReviewToken(APIView):
  def get(self, request):
    user = request.user
    applied = Item.objects.filter(writer=user.usernumber)
    reviews = []
    for e in applied:
      for r in Review.objects.filter(numItem=e.itemnumber):
        reviews.append(r)
    if (not reviews):
      return Response({})
    return Response(ReviewOverviewSerializer(reviews, many=True).data)

class GetReviewItemNumber(APIView):
  def get(self, request, itemNum, order):
    if (order):
      target = Review.objects.filter(numItem=itemNum).order_by('-score')
    else:
      target = Review.objects.filter(numItem=itemNum).order_by('score')
    if (len(target) == 1):
      return Response(ReviewForItemSerializer(target).data)
    return Response(ReviewForItemSerializer(target, many=True).data)