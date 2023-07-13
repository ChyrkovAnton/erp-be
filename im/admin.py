from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from .models import Good, GoodsCategory, UoM, GoodsCharacteristic, Price, \
    PriceType, GoodCharacteristicType


@admin.register(Good)
class GoodAdmin(admin.ModelAdmin):
    list_display = ('id', 'public_id', 'name', 'good_category', 'good_type')


@admin.register(UoM)
class UoMAdmin(admin.ModelAdmin):
    list_display = ('id', 'uom_short_name', 'uom_full_name')


@admin.register(GoodsCharacteristic)
class GoodsCharacteristicsAdmin(admin.ModelAdmin):
    list_display = ('id', 'characteristics_type', 'good', 'uom',
                    'characteristics_value')


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
    list_display = ('characteristics_full_name', 'characteristics_short_name',
                    'priority')





