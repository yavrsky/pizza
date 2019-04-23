from django.urls import path, include
from .views import *
urlpatterns = [
    path('', Constructor.as_view(), name='constructor'),
    path('order/<str:url_order>/', OrderPizza.as_view(), name='order-pizza'),
    path('send/<str:url_order>/<str:total_price>', send, name='send-email')
]
