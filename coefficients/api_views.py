"""
DRF ViewSets for COEFFICIENTS app
"""
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import Coefficient, Metric, Formula, Rule
from .serializers import CoefficientSerializer, MetricSerializer, FormulaSerializer, RuleSerializer


class CoefficientViewSet(viewsets.ModelViewSet):
    queryset = Coefficient.objects.all()
    serializer_class = CoefficientSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['value_type', 'is_active']
    search_fields = ['name', 'code', 'description']
    ordering = ['name']


class MetricViewSet(viewsets.ModelViewSet):
    queryset = Metric.objects.all()
    serializer_class = MetricSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['aggregation_type', 'is_active']
    search_fields = ['name', 'code']
    ordering = ['name']


class FormulaViewSet(viewsets.ModelViewSet):
    queryset = Formula.objects.all()
    serializer_class = FormulaSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name', 'description']
    ordering = ['name']


class RuleViewSet(viewsets.ModelViewSet):
    queryset = Rule.objects.all()
    serializer_class = RuleSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['condition_type', 'is_active']
    search_fields = ['name']
    ordering = ['name']
