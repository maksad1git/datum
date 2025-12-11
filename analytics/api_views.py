"""
DRF ViewSets for ANALYTICS app
"""
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import Dashboard, Report, ReportTemplate, FilterPreset, ForecastModel
from .serializers import (
    DashboardSerializer, ReportSerializer, ReportTemplateSerializer,
    FilterPresetSerializer, ForecastModelSerializer
)


class DashboardViewSet(viewsets.ModelViewSet):
    """ViewSet for Dashboard model"""
    queryset = Dashboard.objects.select_related('owner').prefetch_related('shared_with').all()
    serializer_class = DashboardSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['owner', 'dashboard_type', 'level', 'is_public', 'is_active']
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['name', 'created_at', 'level_order']
    ordering = ['name']


class ReportViewSet(viewsets.ModelViewSet):
    """ViewSet for Report model"""
    queryset = Report.objects.select_related('template', 'created_by').all()
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['template', 'created_by', 'format', 'status']
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'generated_at']
    ordering = ['-created_at']


class ReportTemplateViewSet(viewsets.ModelViewSet):
    """ViewSet for ReportTemplate model"""
    queryset = ReportTemplate.objects.select_related('created_by').prefetch_related('metrics').all()
    serializer_class = ReportTemplateSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['report_type', 'category', 'is_active']
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['name', 'category', 'created_at']
    ordering = ['category', 'name']


class FilterPresetViewSet(viewsets.ModelViewSet):
    """ViewSet for FilterPreset model"""
    queryset = FilterPreset.objects.select_related('owner').all()
    serializer_class = FilterPresetSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['owner', 'applies_to', 'is_public']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['owner', 'name']


class ForecastModelViewSet(viewsets.ModelViewSet):
    """ViewSet for ForecastModel model"""
    queryset = ForecastModel.objects.select_related('created_by').prefetch_related('metrics').all()
    serializer_class = ForecastModelSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['model_type', 'status', 'created_by']
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['name', 'created_at', 'trained_at']
    ordering = ['name']
