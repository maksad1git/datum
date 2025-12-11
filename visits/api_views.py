"""
DRF ViewSets for VISITS app
"""
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import VisitType, Visit, Observation, VisitMedia, Sale
from .serializers import (
    VisitTypeSerializer, VisitSerializer, ObservationSerializer,
    VisitMediaSerializer, SaleSerializer
)


class VisitTypeViewSet(viewsets.ModelViewSet):
    """ViewSet for VisitType model"""
    queryset = VisitType.objects.select_related('form_template').prefetch_related('coefficients').all()
    serializer_class = VisitTypeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type', 'is_active', 'requires_photo', 'requires_signature', 'requires_gps']
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']


class VisitViewSet(viewsets.ModelViewSet):
    """ViewSet for Visit model"""
    queryset = Visit.objects.select_related('visit_type', 'outlet', 'user').all()
    serializer_class = VisitSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['visit_type', 'outlet', 'user', 'status', 'data_source_type']
    search_fields = ['outlet__name', 'user__username', 'notes']
    ordering_fields = ['planned_date', 'start_date', 'end_date', 'created_at']
    ordering = ['-created_at']


class ObservationViewSet(viewsets.ModelViewSet):
    """ViewSet for Observation model"""
    queryset = Observation.objects.select_related('visit', 'coefficient', 'product').all()
    serializer_class = ObservationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['visit', 'coefficient', 'product', 'data_source_type']
    search_fields = ['notes', 'value_text']
    ordering_fields = ['created_at']
    ordering = ['visit', 'coefficient']


class VisitMediaViewSet(viewsets.ModelViewSet):
    """ViewSet for VisitMedia model"""
    queryset = VisitMedia.objects.select_related('visit', 'observation').all()
    serializer_class = VisitMediaSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['visit', 'observation', 'media_type']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']
    ordering = ['visit', 'created_at']


class SaleViewSet(viewsets.ModelViewSet):
    """ViewSet for Sale model"""
    queryset = Sale.objects.select_related('outlet', 'product', 'recorded_by').all()
    serializer_class = SaleSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['outlet', 'product', 'recorded_by']
    search_fields = ['product__name', 'outlet__name']
    ordering_fields = ['sale_date', 'recorded_at', 'total_amount']
    ordering = ['-sale_date']
