from django.urls import path

from . import views

urlpatterns = [
    path('apply/', views.Apply.as_view()),
    path('item/<int:param>/', views.GetItem.as_view()),
    path('item/category/<int:param>/', views.GetItemWithCategory.as_view()),

    #개발 확인용
    path('items/chk/', views.Chk.as_view())
]
