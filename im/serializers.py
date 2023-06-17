from rest_framework import serializers
from .models import GoodsCategory, Good


class GoodsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = ['id', 'name']


class GoodsSubCategoryRecursiveSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        serializer = self.parent.parent.__class__(instance, context=self.context)
        return serializer.data


class GoodsCategorySerializerTree(serializers.ModelSerializer):
    subcategories = GoodsSubCategoryRecursiveSerializer(many=True, read_only=True)

    class Meta:
        model = GoodsCategory
        fields = ('id', 'name', 'subcategories')


class GoodsSerializer(serializers.ModelSerializer):
    current_price = serializers.SerializerMethodField('get_current_price')

    def get_current_price (self, obj):
        prices = obj.prices.all()
        if prices:
            return str(prices.filter(price_type='1').order_by('-price_date').first().value)
        return '0.00'

    class Meta:
        model = Good
        fields = ['id', 'name', 'good_image', 'description', 'current_price']


