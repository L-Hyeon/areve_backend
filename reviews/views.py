from unicodedata import category
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ItemSerializer, ItemSearchSerializer, ReviewSerializer
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
  def post(self, request, reviewNum):
    target = Review.objects.get(reviewnumber = reviewNum)
    return Response(ReviewSerializer(target, many=True).data)
