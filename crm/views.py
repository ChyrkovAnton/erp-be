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

    def format_city(po_object):
        if po_object.city_description.find('(') >= 0:
            return po_object.city_description[:po_object.city_description.find('(')].strip()
        return po_object.city_description.strip()

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
    cities = list(set([format_city(post_office) for post_office in queryset]))
    cities.sort()
    return JsonResponse({'cities': cities})


def offices_by_city(request):
    queryset = []

    def format_po(po_object):
        post_office = po_object.short_address[po_object.short_address.find(' '):]
        return f'№{po_object.number} {post_office.strip()}'

    if request.GET.get('type') == '0':
        queryset = list(PostOffice.objects
                        .exclude(warehouse_category='Postomat')
                        .filter(city_description=request.GET.get('locality'))
                        )
    if request.GET.get('type') == '1':
        queryset = list(PostOffice.objects
                        .filter(warehouse_category='Postomat')
                        .filter(city_description=request.GET.get('locality'))
                        )
    po = list(set([format_po(post_office) for post_office in queryset]))
    po.sort()
    return JsonResponse({'po': po})










