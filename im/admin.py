from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from .models import Good, GoodsCategory, UoM, GoodsCharacteristics, Price, PriceType


@admin.register(Good)
class GoodAdmin(admin.ModelAdmin):
    list_display = ('id', 'public_id', 'name', 'good_category', 'good_type')


@admin.register(UoM)
class UoMAdmin(admin.ModelAdmin):
    pass


@admin.register(GoodsCharacteristics)
class GoodsCharacteristicsAdmin(admin.ModelAdmin):
    pass


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





