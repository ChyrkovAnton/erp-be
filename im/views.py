from rest_framework import generics
from .models import GoodsCategory, Good
from .serializers import GoodsCategorySerializer, GoodsCategorySerializerTree, \
     GoodsSerializer


class GoodsCategoriesAPIView(generics.ListAPIView, generics.CreateAPIView):
    queryset = GoodsCategory.objects.all()
    serializer_class = GoodsCategorySerializer


class GoodsCategoriesAPIViewTree(generics.ListAPIView):
    queryset = GoodsCategory.objects.filter(category_parent_id=None)
    serializer_class = GoodsCategorySerializerTree


class GoodsAPIView(generics.ListAPIView, generics.CreateAPIView):
    queryset = Good.objects.all()
    serializer_class = GoodsSerializer





