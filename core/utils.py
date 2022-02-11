from rest_framework.authtoken.models import Token
from rest_framework.response import Response

def loginDecorator(func):
  def wrapper(self, request, *args, **kwargs):
    user = request.user
    token = Token.objects.get(user=user)
    if (token is None):
      return Response({"Access Denied"})
    return func(self, request, *args, **kwargs)

  return wrapper