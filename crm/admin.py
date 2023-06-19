from django.contrib import admin
from .models import OrderStatus, Order, StatusChange, OrderLine, PostCompany, \
                    PostOffice, OrderDestination


@admin.register(OrderStatus)
class OrderStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'status_name', 'is_active', 'description')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_number', 'order_place_point', 'discount',
                    'user', 'additional_information')


@admin.register(StatusChange)
class StatusChangeAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'status_change_point', 'user')


@admin.register(OrderLine)
class OrderLineAdmin(admin.ModelAdmin):
    list_display = ('id', 'public_id', 'order', 'good', 'quantity', 'price')


@admin.register(PostCompany)
class PostCompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active')


@admin.register(PostOffice)
class PostOfficeAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'zip', 'locality_type', 'locality',
                    'max_weight', 'is_active')


@admin.register(OrderDestination)
class OrderDestinationAdmin(admin.ModelAdmin):
    list_display = ('id', 'post_office', 'region', 'district', 'street_type',
                    'street', 'building', 'apartment')
