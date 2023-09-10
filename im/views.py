from rest_framework import generics
from django.http import JsonResponse
from rest_framework.utils import json
from django.views.decorators.csrf import csrf_exempt
from .models import GoodsCategory, Good, UoM, GoodCharacteristicType, \
     GoodsCharacteristic, GoodsFeature
from .serializers import GoodsCategorySerializer, GoodsCategorySerializerTree, \
     UoMSerializer, GoodCharacteristicTypeSerializer, \
     GoodsCharacteristicSerializer, GoodsSerializer, GoodsFeatureSerializer
from .services import get_price_range, \
    get_goods_queryset_filtered_by_category, get_current_price, \
    create_category_characteristics_response, get_goods_queryset_bound_by_price, \
    get_goods_queryset_filtered_by_features, get_active_features


class GoodsCategoriesAPIView(generics.ListAPIView, generics.CreateAPIView):
    queryset = GoodsCategory.objects.all()
    serializer_class = GoodsCategorySerializer


class GoodsCategoriesAPIViewTree(generics.ListAPIView):
    queryset = GoodsCategory.objects.filter(category_parent_id=None)
    serializer_class = GoodsCategorySerializerTree


class GoodsAPIView(generics.ListAPIView, generics.CreateAPIView):
    serializer_class = GoodsSerializer

    def get_queryset(self):
        request = self.request
        goods_filtered_by_category = get_goods_queryset_filtered_by_category(request)
        goods_filtered_by_price = get_goods_queryset_bound_by_price(request, goods_filtered_by_category)
        goods_filtered_by_features = get_goods_queryset_filtered_by_features(request, goods_filtered_by_price)
        return goods_filtered_by_features


class UoMAPIView(generics.ListAPIView):
    queryset = UoM.objects.all()
    serializer_class = UoMSerializer


class GoodCharacteristicTypeAPIView(generics.ListAPIView):
    queryset = GoodCharacteristicType.objects.all()
    serializer_class = GoodCharacteristicTypeSerializer


class GoodsCharacteristicAPIView(generics.ListAPIView):
    queryset = GoodsCharacteristic.objects.all()
    serializer_class = GoodsCharacteristicSerializer


@csrf_exempt
def get_filtered_goods_list(request):
    characteristics = json.loads(request.GET.get('filters'))['characteristics']
    for c in characteristics:
        print(c)
    return JsonResponse({'filters': json.loads(request.GET.get('filters'))})


class GoodsFeatureAPIView(generics.ListAPIView):
    queryset = GoodsFeature.objects.all()
    serializer_class = GoodsFeatureSerializer


def send_category_characteristics(request):
    return JsonResponse(create_category_characteristics_response(request))


def send_active_features(request):
    return JsonResponse(get_active_features(request))






