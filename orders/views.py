from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import OrderSerializer
from core.utils import loginDecorator
import json
from .models import Order

class MakeOrder(APIView):
  @loginDecorator
  def post(self, request):
    data = json.loads(request.body)
    order = Order.objects.create_order(
      seller = data["seller"],
      buyer = request.user.usernumber,
      itemnumber = data["itemnumber"],
      startTime= data["startTime"],
      endTime = data["endTime"],
      price = data["price"],
      buyerName = data["name"],
      buyerPhone = data["phone"],
      buyerEmail = data["email"],
      buyerDemand = data["demand"]
    )

    return Response(order.ordernumber)

class GetOrder(APIView):
  @loginDecorator
  def get(self, request, orderNum):
    target = Order.objects.get(ordernumber = orderNum)
    return Response(OrderSerializer(target).data)
