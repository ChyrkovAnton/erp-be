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
    create_category_characteristics_response


class GoodsCategoriesAPIView(generics.ListAPIView, generics.CreateAPIView):
    queryset = GoodsCategory.objects.all()
    serializer_class = GoodsCategorySerializer


class GoodsCategoriesAPIViewTree(generics.ListAPIView):
    queryset = GoodsCategory.objects.filter(category_parent_id=None)
    serializer_class = GoodsCategorySerializerTree


class GoodsAPIView(generics.ListAPIView, generics.CreateAPIView):
    serializer_class = GoodsSerializer

    def get_queryset(self):
        category = self.request.GET.get('category_id')
        if self.request.GET.get('filters'):
            filters = json.loads(self.request.GET.get('filters'))
            characteristics = filters['characteristics']
            prices = filters['prices']
            category_filtered_goods = Good.objects.filter(good_category=category)
            price_filtered_goods = []
            for good in category_filtered_goods:
                price = float(get_current_price(good))
                if float(prices['min_price']) <= price <= float(prices['max_price']):
                    price_filtered_goods.append(good.id)
            return Good.objects.filter(id__in=price_filtered_goods)
        if category:
            if category == '1':
                return Good.objects.all()
            return Good.objects.filter(good_category=category)


class UoMAPIView(generics.ListAPIView):
    queryset = UoM.objects.all()
    serializer_class = UoMSerializer


class GoodCharacteristicTypeAPIView(generics.ListAPIView):
    queryset = GoodCharacteristicType.objects.all()
    serializer_class = GoodCharacteristicTypeSerializer


class GoodsCharacteristicAPIView(generics.ListAPIView):
    queryset = GoodsCharacteristic.objects.all()
    serializer_class = GoodsCharacteristicSerializer


# def get_category_characteristics_n(request):
#     return JsonResponse({'characteristics': get_category_goods_characteristics(request),
#                          'prices': get_price_range(get_goods_queryset_filtered_by_category(request))})


@csrf_exempt
def get_filtered_goods_list(request):
    characteristics = json.loads(request.GET.get('filters'))['characteristics']
    for c in characteristics:
        print(c)
    return JsonResponse({'filters': json.loads(request.GET.get('filters'))})


class GoodsFeatureAPIView(generics.ListAPIView):
    queryset = GoodsFeature.objects.all()
    serializer_class = GoodsFeatureSerializer


def get_category_characteristics(request):
    return JsonResponse(create_category_characteristics_response(request))






