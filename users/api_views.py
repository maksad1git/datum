"""
DRF ViewSets for USERS app
"""
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import User, Role, Permission, UserSession
from .serializers import UserSerializer, RoleSerializer, PermissionSerializer, UserSessionSerializer


class RoleViewSet(viewsets.ModelViewSet):
    """ViewSet for Role model"""
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'code']
    ordering_fields = ['name']
    ordering = ['name']


class PermissionViewSet(viewsets.ModelViewSet):
    """ViewSet for Permission model"""
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'code']
    ordering_fields = ['name']
    ordering = ['name']


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for User model"""
    queryset = User.objects.select_related('role').all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['role', 'is_active', 'is_staff']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering_fields = ['username', 'date_joined']
    ordering = ['username']


class UserSessionViewSet(viewsets.ModelViewSet):
    """ViewSet for UserSession model"""
    queryset = UserSession.objects.select_related('user').all()
    serializer_class = UserSessionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['user']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
