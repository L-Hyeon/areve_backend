from django.contrib import auth
from .serializers import UserSerializer, OtherUserSerializer
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import User
from items.models import Item
from core.utils import loginDecorator
import json

class Signup(APIView):
  def post(self, request):
    data = json.loads(request.body.decode('utf-8'))
    user = User.objects.create_user(
      email = data["email"],
      name = data["name"],
      nickname = data["nickname"],
      birth = data["birth"],
      phonenumber = data["phone"],
      password = data["password"],
      location = data["location"],
      sigungu = data["sigungu"],
      postcode = data["postcode"]
    )
    token = Token.objects.create(user=user)
    return Response({"Token": token.key, "Like": user.like})

class Login(APIView):
  def post(self, request):
    data = json.loads(request.body)
    user = auth.authenticate(username=data["email"], password=data["password"])
    if (user is not None):
      token = Token.objects.get(user=user)
      if (token is None):
        token = Token.objects.create(user=user)
      return Response({"Token": token.key, "Like": user.like})
    else:
      return Response(status=401)

class Logout(APIView):
  @loginDecorator
  def get(self, request):
    user = request.user
    token = Token.objects.get(user=user)
    token.delete()
    return Response({"Logout"})

class ChangePassword(APIView):
  @loginDecorator
  def post(self, request):
    data = json.loads(request.body)
    newPassword = data["newPassword"]
    user = request.user
    user.set_password(newPassword)
    user.save()
    
    #Change Token
    token = Token.objects.get(user=user)
    token.delete()
    token = Token.objects.create(user=user)
    return Response({"Token": token.key})

class Like(APIView):
  @loginDecorator
  def get(self, request, itemNum):
    user = request.user
    item = Item.objects.get(itemnumber=itemNum)
    item.like += 1
    item.save()
    user.like += str(itemNum) + ' '
    user.save()
    return Response({"Like": user.like})

class Dislike(APIView):
  @loginDecorator
  def get(self, request, itemNum):
    user = request.user
    item = Item.objects.get(itemnumber=itemNum)
    item.like -= 1
    item.save()
    like = user.like.split()
    print(like, itemNum)
    try:
      like.remove(str(itemNum))
      print(like)
      user.like = ' '.join(like) + ' '
      user.save()
      print(user.like)
      return Response({"Like": user.like})
    except:
      return Response(status=404, data={"msg": "Already Deleted"})

class GetUser(APIView):
  def get(self, request, usernumber):
    target = User.objects.get(usernumber=usernumber)
    return Response(OtherUserSerializer(target).data)

class GetUserWithToken(APIView):
  def get(self, request):
    user = request.user
    return Response(UserSerializer(user).data)

class SetUserLocation(APIView):
  def post(self, request):
    data = json.loads(request.body)
    user = request.user
    user.location = data["location"]
    user.postcode = data["postcode"]
    user.sigungu = data["sigungu"]
    user.save()
    return Response({"loc": user.location, "po": user.postcode, "si": user.sigungu})
