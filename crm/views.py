from django.http import JsonResponse, HttpResponse
from rest_framework import generics
from .models import OrderStatus, Order, StatusChange, OrderLine, PostCompany, \
                    PostOffice, OrderDestination
from .serializers import OrderStatusSerializer, OrderLineSerializer, \
    OrderSerializer, OrderSerializerCreate, CitiesPostOfficeSerializer
from .services import get_customer_statistics


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
    queryset = PostOffice.objects.filter(settlement_area_description=request.GET.get('region'))
    print(type(queryset))

    def format_city(po_object):
        if po_object.city_description.find('(') >= 0:
            return po_object.city_description[:po_object.city_description.find('(')].strip()
        return po_object.city_description.strip()

    if request.GET.get('type') == '0':
        queryset = list(queryset.exclude(warehouse_category='Postomat'))
    if request.GET.get('type') == '1':
        queryset = list(queryset.filter(warehouse_category='Postomat'))
    cities = list(set([format_city(post_office) for post_office in queryset]))
    cities.sort()
    return JsonResponse({'cities': cities})


def offices_by_city(request):
    queryset = PostOffice.objects\
        .filter(settlement_area_description=request.GET.get('region'))\
        .filter(city_description__startswith=request.GET.get('locality'))

    def format_po(po_object):
        post_office = po_object.short_address[po_object.short_address.find(' '):]
        return f'№{po_object.number} {post_office.strip()}'

    if request.GET.get('type') == '0':
        queryset = list(queryset.exclude(warehouse_category='Postomat'))
    if request.GET.get('type') == '1':
        queryset = list(queryset.filter(warehouse_category='Postomat'))
    po = list(set([format_po(post_office) for post_office in queryset]))
    po.sort()
    return JsonResponse({'po': po})


def provide_customer_statistics(request, **kwargs):
    return JsonResponse({'statistics': get_customer_statistics(request, **kwargs)})










