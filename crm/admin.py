from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import OrderStatus, Order, StatusChange, OrderLine, PostCompany, \
                    PostOffice, OrderDestination


@admin.register(OrderStatus)
class OrderStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'status_name', 'is_active', 'description')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_number', 'order_place_point', 'discount',
                    'additional_information', 'customer_first_name',
                    'customer_last_name', 'is_paid')


@admin.register(StatusChange)
class StatusChangeAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'status_change_point', 'user')


@admin.register(OrderLine)
class OrderLineAdmin(admin.ModelAdmin):
    list_display = ('id', 'public_id', 'order', 'good', 'quantity', 'price')


@admin.register(OrderDestination)
class OrderDestinationAdmin(admin.ModelAdmin):
    list_display = ('id', 'post_office', 'region', 'district', 'street_type',
                    'street', 'building', 'apartment')


@admin.register(PostOffice)
class PostOfficeAdmin(ImportExportModelAdmin):
    list_display = ('id',
                    'post',
                    'nova_poshta_key',
                    'short_address',
                    'short_address_ru',
                    'number',
                    'city_description',
                    'city_description_ru',
                    'settlement_description',
                    'settlement_area_description',
                    'settlement_region_description',
                    'settlement_type_description',
                    'settlement_type_description_ru',
                    'longitude',
                    'latitude',
                    'max_weight',
                    'warehouse_category',
                    'is_active',
                    )


    @admin.register(PostCompany)
    class PostCompanyAdmin(admin.ModelAdmin):
        list_display = ('id',
                        'public_id',
                        'name',
                        'is_active'
                        )
