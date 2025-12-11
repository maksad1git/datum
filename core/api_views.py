from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import SystemSettings, IntegrationSettings, SystemLog, AuditLog
from .serializers import SystemSettingsSerializer, IntegrationSettingsSerializer, SystemLogSerializer, AuditLogSerializer

class SystemSettingsViewSet(viewsets.ModelViewSet):
    queryset = SystemSettings.objects.all()
    serializer_class = SystemSettingsSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['key', 'description']

class IntegrationSettingsViewSet(viewsets.ModelViewSet):
    queryset = IntegrationSettings.objects.all()
    serializer_class = IntegrationSettingsSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['is_active']
    search_fields = ['name', 'provider']

class SystemLogViewSet(viewsets.ModelViewSet):
    queryset = SystemLog.objects.all()
    serializer_class = SystemLogSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['level']
    search_fields = ['message']
    ordering = ['-created_at']

class AuditLogViewSet(viewsets.ModelViewSet):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['user', 'action', 'model_name']
    search_fields = ['model_name', 'changes']
    ordering = ['-timestamp']
