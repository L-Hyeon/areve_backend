from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ReviewForItemSerializer, ReviewOverviewSerializer, ReviewSerializer
from core.utils import loginDecorator
import json
from .models import Review
from items.models import Item
from items.serializers import ItemReviewSerializer

class WriteReview(APIView):
  def post(self, request):
    data = json.loads(request.body)
    images = data["images"]
    for i in range(data["cntImg"], 6):
      images += ['']
    review = Review.objects.create_review(
      score = data["score"],
      content = data["content"],
      cntImg = data["cntImg"],
      images = images,
      numItem = data["itemnumber"],
      numWriter = data["usernumber"],
      writerName = data["username"]
    )
    return Response(review.reviewnumber)

class GetReview(APIView):
  def get(self, request, reviewNum):
    target = Review.objects.get(reviewnumber = reviewNum)
    item = Item.objects.get(itemnumber=target.numItem)
    ret = [ReviewSerializer(target).data, ItemReviewSerializer(item).data]
    return Response(ret)

class GetReviewUserNumber(APIView):
  def get(self, request, userNum):
    target = Review.objects.filter(numWriter=userNum)
    if (len(target) == 1):
      return Response(ReviewOverviewSerializer(target).data)
    return Response(ReviewOverviewSerializer(target, many=True).data)

class GetReviewToken(APIView):
  def get(self, request):
    user = request.user
    target = Review.objects.filter(numWriter=user.usernumber)
    if (len(target) == 1):
      return Response(ReviewOverviewSerializer(target).data)
    return Response(ReviewOverviewSerializer(target, many=True).data)

class GetReviewItemNumber(APIView):
  def get(self, request, itemNum, order):
    if (order):
      target = Review.objects.filter(numItem=itemNum).order_by('-score')
    else:
      target = Review.objects.filter(numItem=itemNum).order_by('score')
    if (len(target) == 1):
      return Response(ReviewForItemSerializer(target).data)
    return Response(ReviewForItemSerializer(target, many=True).data)