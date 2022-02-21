from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ReviewOverviewSerializer, ReviewSerializer
from core.utils import loginDecorator
import json
from .models import Review

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
      numWriter = data["usernumber"]
    )
    return Response(review.reviewnumber)

class GetReview(APIView):
  def get(self, request, reviewNum):
    target = Review.objects.get(reviewnumber = reviewNum)
    return Response(ReviewSerializer(target).data)

class GetReviewUserNumber(APIView):
  def get(self, request, userNum):
    target = Review.objects.filter(numWriter=userNum)
    return Response(ReviewOverviewSerializer(target, many=True).data)

class GetReviewToken(APIView):
  def get(self, request):
    user = request.user
    target = Review.objects.filter(numWriter=user.usernumber)
    return Response(ReviewOverviewSerializer(target, many=True).data)