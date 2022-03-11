from django.urls import path

from . import views

urlpatterns = [
  path('makeorder/', views.MakeOrder.as_view()),
  path('order/<int:orderNum>', views.GetOrder.as_view()),
]
