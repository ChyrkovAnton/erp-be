from rest_framework import serializers
from .models import Comment


class CommentSerializer (serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.username', read_only=True)
    id = serializers.UUIDField(source='public_id', read_only=True, format='hex')
    parent = serializers.UUIDField(source='parent.public_id', read_only=True, format='hex')
    customer = serializers.UUIDField(source='customer.public_id', read_only=True, format='hex')

    class Meta:
        model = Comment
        fields = ['id', 'parent', 'good', 'customer', 'customer_name', 'text', 'created']

