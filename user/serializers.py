from rest_framework import serializers
from .models import User


class UserSerializer (serializers.ModelSerializer):
    id = serializers.UUIDField(source='public_id', read_only=True, format='hex')

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'middle_name', 'last_name',
                  'birthday', 'gender', 'email', 'phone', 'is_active']
        read_only_field = ['is_active']