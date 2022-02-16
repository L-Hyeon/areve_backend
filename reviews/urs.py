from django.urls import path

from . import views

urlpatterns = [
    path('writeReview/', views.WriteReview.as_view()),
    path('review/<int:reviewNum>/', views.GetReview.as_view()),
]
