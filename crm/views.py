from rest_framework import generics
from .models import OrderStatus, Order, StatusChange, OrderLine, PostCompany, \
                    PostOffice, OrderDestination
from .serializers import OrderStatusSerializer, OrderLineSerializer, \
    OrderSerializer, OrderSerializerCreate


class OrderStatusAPIView(generics.ListAPIView, generics.CreateAPIView):
    queryset = OrderStatus.objects.all()
    serializer_class = OrderStatusSerializer


class OrderLineAPIView(generics.ListAPIView, generics.CreateAPIView):
    queryset = OrderLine.objects.all()
    serializer_class = OrderLineSerializer


class OrderAPIView(generics.ListAPIView, generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_serializer_class(self):
        if self.request.method in ["POST", "UPDATE"]:
            return OrderSerializerCreate
        return self.serializer_class


