from django.urls import path

from . import views

urlpatterns = [
    path('signup/', views.Signup.as_view()),
    path('login/', views.Login.as_view()),
    path('logout/', views.Logout.as_view()),
    path('changePW/', views.ChangePassword.as_view()),
    path('tokenChk/', views.TokenChk.as_view()),


    #개발 확인용
    path('chk/', views.Chk.as_view())
]
