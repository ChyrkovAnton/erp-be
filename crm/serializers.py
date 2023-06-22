from rest_framework import serializers
from .models import OrderStatus, Order, StatusChange, OrderLine, PostCompany, \
                    PostOffice, OrderDestination


class OrderStatusSerializer (serializers.ModelSerializer):
    id = serializers.UUIDField(source='public_id', read_only=True, format='hex')

    class Meta:
        model = OrderStatus
        fields = ['id', 'status_name', 'description', 'is_active']


class OrderLineSerializer (serializers.ModelSerializer):

    class Meta:
        model = OrderLine
        fields = ['id', 'order', 'good', 'quantity', 'price']
        extra_kwargs = {'order': {'required': False}}


class OrderSerializer (serializers.ModelSerializer):
    id = serializers.UUIDField(source='public_id', read_only=True, format='hex')
    order_lines = OrderLineSerializer(source='order_line_order', many=True)

    class Meta:
        model = Order
        fields = ['id', 'order_number', 'order_place_point', 'discount',
                  'additional_information', 'customer_first_name',
                  'customer_middle_name', 'customer_last_name',
                  'customer_phone', 'customer_email', 'order_lines']


class OrderSerializerCreate(OrderSerializer):
    order_lines = OrderLineSerializer(many=True)

    def create(self, validated_data):
        lines = validated_data.pop('order_lines')
        order = Order.objects.create(**validated_data)
        for line in lines:
            OrderLine.objects.create(order=order, **line)
        order.order_lines = list(order.order_line_order.all())
        return order


class CitiesPostOfficeSerializer (serializers.ModelSerializer):

    class Meta:
        model = PostOffice
        fields = ['city_description']
