from rest_framework import generics
from django.http import JsonResponse
from .models import GoodsCategory, Good, UoM, GoodCharacteristicType, \
     GoodsCharacteristic
from .serializers import GoodsCategorySerializer, GoodsCategorySerializerTree, \
     GoodsSerializer, UoMSerializer, GoodCharacteristicTypeSerializer, \
     GoodsCharacteristicSerializer
from .services import get_category_goods_characteristics, get_price_range, \
    get_category_goods


class GoodsCategoriesAPIView(generics.ListAPIView, generics.CreateAPIView):
    queryset = GoodsCategory.objects.all()
    serializer_class = GoodsCategorySerializer


class GoodsCategoriesAPIViewTree(generics.ListAPIView):
    queryset = GoodsCategory.objects.filter(category_parent_id=None)
    serializer_class = GoodsCategorySerializerTree


class GoodsAPIView(generics.ListAPIView, generics.CreateAPIView):
    queryset = Good.objects.all()
    serializer_class = GoodsSerializer


class UoMAPIView(generics.ListAPIView):
    queryset = UoM.objects.all()
    serializer_class = UoMSerializer


class GoodCharacteristicTypeAPIView(generics.ListAPIView):
    queryset = GoodCharacteristicType.objects.all()
    serializer_class = GoodCharacteristicTypeSerializer


class GoodsCharacteristicAPIView(generics.ListAPIView):
    queryset = GoodsCharacteristic.objects.all()
    serializer_class = GoodsCharacteristicSerializer


def get_category_characteristics(request):
    return JsonResponse({'characteristics': get_category_goods_characteristics(request),
                         'prices': get_price_range(get_category_goods(request))})










