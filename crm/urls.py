from django.urls import path
from .views import OrderStatusAPIView, OrderLineAPIView, OrderAPIView, \
    cities_by_region, offices_by_city


urlpatterns = [
    path('order_status/', OrderStatusAPIView.as_view()),
    path('order_lines/', OrderLineAPIView.as_view()),
    path('orders/', OrderAPIView.as_view()),
    path('cities/', cities_by_region),
    path('po/', offices_by_city),
]