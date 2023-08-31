from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from .models import Good, GoodsCategory, UoM, GoodsCharacteristic, Price, \
    PriceType, GoodCharacteristicType, GoodsFeature


@admin.register(GoodsCharacteristic)
class GoodsCharacteristicsAdmin(admin.ModelAdmin):
    list_display = ('id', 'characteristic_type', 'good', 'uom',
                    'characteristic_value')


class GoodsCharacteristicInline(admin.TabularInline):
    model = GoodsCharacteristic
    extra = 0


class PriceInline(admin.TabularInline):
    model = Price
    extra = 0


class GoodsFeatureInline(admin.TabularInline):
    model = Good.goodsfeature_set.through
    extra = 0


@admin.register(Good)
class GoodAdmin(admin.ModelAdmin):
    list_display = ('id', 'public_id', 'name', 'good_category', 'good_type', 'get_features')
    list_display_links = ('id', 'public_id', 'name', 'good_category', 'good_type', 'get_features')
    inlines = [
        GoodsCharacteristicInline,
        PriceInline,
        GoodsFeatureInline
    ]

    def get_features(self, instance):
        return [feature for feature in instance.goodsfeature_set.all()]


@admin.register(UoM)
class UoMAdmin(admin.ModelAdmin):
    list_display = ('id', 'uom_short_name', 'uom_full_name')


@admin.register(GoodsCategory)
class GoodsCategoryAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title',)
    list_display_links = ('indented_title',)


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = ('good', 'price_type', 'price_date', 'value')


@admin.register(PriceType)
class PriceTypeAdmin(admin.ModelAdmin):
    list_display = ('price_type', 'description', 'calculation')


@admin.register(GoodCharacteristicType)
class CharacteristicTypeAdmin(admin.ModelAdmin):
    list_display = ('characteristic_full_name', 'characteristic_short_name',
                    'priority')


@admin.register(GoodsFeature)
class GoodsFeatureAdmin(admin.ModelAdmin):
    list_display = ('id', 'characteristic_type', 'uom', 'characteristic_value')



