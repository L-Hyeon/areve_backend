from django.urls import path

from . import views

urlpatterns = [
    path('signup/', views.Signup.as_view()),
    path('login/', views.Login.as_view()),
    path('logout/', views.Logout.as_view()),
    path('changePW/', views.ChangePassword.as_view()),
    path('user/<int:usernumber>/', views.GetUser.as_view()),
    path('user/token', views.GetUserWithToken.as_view()),
    path('like/<int:itemNum>', views.Like.as_view()),

    #개발 확인용
    path('accounts/chk/', views.Chk.as_view())
]
