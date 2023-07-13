from rest_framework import generics
from .models import GoodsCategory, Good, UoM, GoodCharacteristicType, \
     GoodsCharacteristic
from .serializers import GoodsCategorySerializer, GoodsCategorySerializerTree, \
     GoodsSerializer, UoMSerializer, GoodCharacteristicTypeSerializer, \
     GoodsCharacteristicSerializer


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








