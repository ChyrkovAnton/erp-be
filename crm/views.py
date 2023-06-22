from django.http import JsonResponse, HttpResponse
from rest_framework import generics
from .models import OrderStatus, Order, StatusChange, OrderLine, PostCompany, \
                    PostOffice, OrderDestination
from .serializers import OrderStatusSerializer, OrderLineSerializer, \
    OrderSerializer, OrderSerializerCreate, CitiesPostOfficeSerializer


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


def cities_by_region(request):
    queryset = []
    if request.GET.get('type') == '0':
        queryset = list(PostOffice.objects
                        .exclude(warehouse_category='Postomat')
                        .filter(settlement_area_description=request.GET.get('region'))
                        )
    if request.GET.get('type') == '1':
        queryset = list(PostOffice.objects
                        .filter(warehouse_category='Postomat')
                        .filter(settlement_area_description=request.GET.get('region'))
                        )
    cities = list(set([po.city_description for po in queryset]))
    cities.sort()

    return JsonResponse({'cities': cities})









