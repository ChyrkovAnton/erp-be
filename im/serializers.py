from rest_framework import serializers
from .models import GoodsCategory, Good, UoM, GoodCharacteristicType, \
    GoodsCharacteristic, GoodsFeature


class UoMSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='public_id', read_only=True, format='hex')

    class Meta:
        model = UoM
        fields = ['id', 'uom_full_name', 'uom_short_name']


class UoMDetailSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.UUIDField(source='public_id', read_only=True, format='hex')

    class Meta:
        model = UoM
        fields = ['id', 'uom_full_name', 'uom_short_name']


class GoodCharacteristicTypeSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='public_id', read_only=True, format='hex')

    class Meta:
        model = GoodCharacteristicType
        fields = ['id', 'characteristic_full_name', 'characteristic_short_name',
                  'priority']


class GoodCharacteristicTypeDetailSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.UUIDField(source='public_id', read_only=True, format='hex')

    class Meta:
        model = GoodCharacteristicType
        fields = ['id', 'characteristic_full_name', 'characteristic_short_name',
                  'priority']


class GoodsCharacteristicSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='public_id', read_only=True, format='hex')
    uom = UoMDetailSerializer(read_only=True)
    characteristics_type = GoodCharacteristicTypeDetailSerializer(read_only=True)

    class Meta:
        model = GoodsCharacteristic
        fields = ['id', 'characteristics_type', 'uom', 'good', 'characteristics_value']


class GoodsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = ['id', 'name', 'category_parent']


class GoodsSubCategoryRecursiveSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        serializer = self.parent.parent.__class__(instance, context=self.context)
        return serializer.data


class GoodsCategorySerializerTree(serializers.ModelSerializer):
    subcategories = GoodsSubCategoryRecursiveSerializer(many=True, read_only=True)

    class Meta:
        model = GoodsCategory
        fields = ('id', 'name', 'subcategories')


class GoodsFeatureSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='public_id', read_only=True, format='hex')
    uom = UoMDetailSerializer(read_only=True)
    characteristic_type = GoodCharacteristicTypeDetailSerializer(read_only=True)

    class Meta:
        model = GoodsFeature
        fields = ['id', 'characteristic_type', 'uom', 'characteristic_value']


class GoodsSerializer(serializers.ModelSerializer):
    category = GoodsCategorySerializer(source='good_category')
    current_price = serializers.SerializerMethodField('get_current_price')
    good_characteristics = GoodsFeatureSerializer(source='goodsfeature_set', read_only=True, many=True)

    def get_current_price (self, obj):
        prices = obj.prices.all()
        if prices:
            return str(prices.filter(price_type='1').order_by('-price_date').first().value)
        return '0.00'

    class Meta:
        model = Good
        fields = ['id', 'name', 'good_image', 'description', 'current_price', 'category', 'good_characteristics']