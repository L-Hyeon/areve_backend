from django.contrib import auth
from .serializers import UserSerializer, OtherUserSerializer
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import User
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
      password = data["password"]
    )
    token = Token.objects.create(user=user)
    return Response({"Token": token.key})

class Login(APIView):
  def post(self, request):
    data = json.loads(request.body)
    user = auth.authenticate(username=data["email"], password=data["password"])
    if (user is not None):
      token = Token.objects.get(user=user)
      if (token is None):
        token = Token.objects.create(user=user)
      return Response({"Token": token.key})
    else:
      return Response(status=401)

class Logout(APIView):
  @loginDecorator
  def get(self, request):
    user = request.user
    Token.objects.delete(user=user)
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
    Token.objects.delete(user=user)
    token = Token.objects.create(user=user)
    return Response({"Token": token})

class Chk(APIView):
  def get(self, request):
    chk = User.objects.all()
    serializer = UserSerializer(chk, many=True)
    return Response(serializer.data)

class GetUser(APIView):
  @loginDecorator
  def get(self, request, usernumber):
    target = User.objects.get(usernumber=usernumber)
    if (usernumber == request.user.usernumber):
      return Response(UserSerializer(target, many=True).data)
    return Response(OtherUserSerializer(target, many=True).data)
