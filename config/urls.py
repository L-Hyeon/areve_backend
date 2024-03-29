from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('', include('items.urls')),
    path('', include('reviews.urls')),
    path('', include('orders.urls'))
]
