from django.urls import path

from . import views

urlpatterns = [
    path('apply/', views.Apply.as_view()),
    path('item/<int:itemnumber>/', views.GetItem.as_view()),
    path('category/<int:catNum>/page/<int:pageNum>', views.GetItemWithCategory.as_view()),
    path('item/main/<int:param>', views.GetItemInMain.as_view()),
    path('item/liked/<int:pageNum>', views.GetItemLiked.as_view()),
    path('item/<int:pageNum>/search', views.GetItemSearch.as_view()),
    path('item/similar/<int:itemNum>', views.GetItemSimilar.as_view()),
    path('item/applied/<int:userNum>/<int:pageNum>', views.GetItemApplied.as_view()),
    path('item/applied/<int:pageNum>', views.GetItemApplied.as_view()),
    path('item/ordered', views.GetItemOrdered.as_view()),

    #개발 확인용
    path('items/chk/', views.Chk.as_view())
]
