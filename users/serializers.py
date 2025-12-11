"""
DRF Serializers for USERS app models
"""
from rest_framework import serializers
from .models import User, Role, Permission, UserSession


class RoleSerializer(serializers.ModelSerializer):
    """Serializer for Role model"""

    class Meta:
        model = Role
        fields = '__all__'


class PermissionSerializer(serializers.ModelSerializer):
    """Serializer for Permission model"""

    class Meta:
        model = Permission
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    role_name = serializers.CharField(source='role.name', read_only=True, allow_null=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'role_name',
                  'is_active', 'is_staff', 'date_joined', 'last_login']
        read_only_fields = ['date_joined', 'last_login']


class UserSessionSerializer(serializers.ModelSerializer):
    """Serializer for UserSession model"""
    user_username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = UserSession
        fields = '__all__'
