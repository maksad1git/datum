"""
DRF ViewSets for GEO app
"""
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import (
    GlobalMarket, Country, Region, City, District, Channel, Outlet,
    FootfallCounter, OutletInventory, Display, DisplayInventory
)
from .serializers import (
    GlobalMarketSerializer, CountrySerializer, RegionSerializer,
    CitySerializer, DistrictSerializer, ChannelSerializer, OutletSerializer,
    FootfallCounterSerializer, OutletInventorySerializer,
    DisplaySerializer, DisplayInventorySerializer
)


class GlobalMarketViewSet(viewsets.ModelViewSet):
    """ViewSet for GlobalMarket model"""
    queryset = GlobalMarket.objects.all()
    serializer_class = GlobalMarketSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'code']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']


class CountryViewSet(viewsets.ModelViewSet):
    """ViewSet for Country model"""
    queryset = Country.objects.select_related('global_market').all()
    serializer_class = CountrySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['global_market', 'data_type']
    search_fields = ['name', 'code']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']


class RegionViewSet(viewsets.ModelViewSet):
    """ViewSet for Region model"""
    queryset = Region.objects.select_related('country__global_market').all()
    serializer_class = RegionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['country', 'data_type']
    search_fields = ['name', 'code']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']


class CityViewSet(viewsets.ModelViewSet):
    """ViewSet for City model"""
    queryset = City.objects.select_related('region__country').all()
    serializer_class = CitySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['region', 'data_type']
    search_fields = ['name', 'code']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']


class DistrictViewSet(viewsets.ModelViewSet):
    """ViewSet for District model"""
    queryset = District.objects.select_related('city__region').all()
    serializer_class = DistrictSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['city', 'data_type']
    search_fields = ['name', 'code']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']


class ChannelViewSet(viewsets.ModelViewSet):
    """ViewSet for Channel model"""
    queryset = Channel.objects.select_related('district__city').all()
    serializer_class = ChannelSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['district', 'channel_type', 'data_type']
    search_fields = ['name', 'code']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']


class OutletViewSet(viewsets.ModelViewSet):
    """ViewSet for Outlet model"""
    queryset = Outlet.objects.select_related('channel').all()
    serializer_class = OutletSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['channel', 'status', 'data_type']
    search_fields = ['name', 'code', 'address']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']


class FootfallCounterViewSet(viewsets.ModelViewSet):
    """ViewSet for FootfallCounter model"""
    queryset = FootfallCounter.objects.select_related('outlet').all()
    serializer_class = FootfallCounterSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['outlet', 'counter_type', 'is_active']
    ordering_fields = ['created_at']
    ordering = ['-created_at']


class OutletInventoryViewSet(viewsets.ModelViewSet):
    """ViewSet for OutletInventory model"""
    queryset = OutletInventory.objects.select_related('outlet', 'product').all()
    serializer_class = OutletInventorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['outlet', 'product']
    ordering_fields = ['last_updated']
    ordering = ['-last_updated']


class DisplayViewSet(viewsets.ModelViewSet):
    """ViewSet for Display model"""
    queryset = Display.objects.select_related('outlet').all()
    serializer_class = DisplaySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['outlet', 'display_type', 'is_active']
    search_fields = ['name', 'location']
    ordering_fields = ['created_at']
    ordering = ['-created_at']


class DisplayInventoryViewSet(viewsets.ModelViewSet):
    """ViewSet for DisplayInventory model"""
    queryset = DisplayInventory.objects.select_related('display', 'product').all()
    serializer_class = DisplayInventorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['display', 'product']
    ordering_fields = ['last_updated']
    ordering = ['-last_updated']
