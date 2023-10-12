from rest_framework import generics
from django.http import JsonResponse
from rest_framework.utils import json
from django.views.decorators.csrf import csrf_exempt
from .models import GoodsCategory, UoM, GoodCharacteristicType, GoodsCharacteristic, \
    GoodsFeature, Good
from .serializers import GoodsCategorySerializer, GoodsCategorySerializerTree, \
    UoMSerializer, GoodCharacteristicTypeSerializer, GoodsCharacteristicSerializer,\
    GoodsSerializer, GoodsFeatureSerializer
from .services import create_category_characteristics_response, get_active_features, \
    filter_goods_by_all_parameters, pivot_goods_features, group_goods_by_category_name, \
    get_wish_list_goods


class GoodsCategoriesAPIView(generics.ListAPIView, generics.CreateAPIView):
    queryset = GoodsCategory.objects.all()
    serializer_class = GoodsCategorySerializer


class GoodsCategoriesAPIViewTree(generics.ListAPIView):
    queryset = GoodsCategory.objects.filter(category_parent_id=None)
    serializer_class = GoodsCategorySerializerTree


class GoodsAPIView(generics.ListAPIView, generics.CreateAPIView):
    serializer_class = GoodsSerializer

    def get_queryset(self):
        return filter_goods_by_all_parameters(self.request)


class WishListGoodsAPIView(generics.ListAPIView):
    serializer_class = GoodsSerializer

    def get_queryset(self):
        return get_wish_list_goods(self.request)


class GoodAPIView(generics.RetrieveAPIView):
    serializer_class = GoodsSerializer

    def get_object(self):
        return Good.objects.get(id=self.kwargs.get('good_id'))


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


def send_goods_pivot(request):
    return JsonResponse(pivot_goods_features(request))


def make_goods_grouped_by_category_name_response(request):
    return JsonResponse({'categories': group_goods_by_category_name(request)})







