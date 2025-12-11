"""
DRF Serializers for GEO app models
"""
from rest_framework import serializers
from .models import (
    GlobalMarket, Country, Region, City, District, Channel, Outlet,
    FootfallCounter, OutletInventory, Display, DisplayInventory
)


class GlobalMarketSerializer(serializers.ModelSerializer):
    """Serializer for GlobalMarket model"""

    class Meta:
        model = GlobalMarket
        fields = '__all__'


class CountrySerializer(serializers.ModelSerializer):
    """Serializer for Country model"""
    global_market_name = serializers.CharField(source='global_market.name', read_only=True)

    class Meta:
        model = Country
        fields = '__all__'


class RegionSerializer(serializers.ModelSerializer):
    """Serializer for Region model"""
    country_name = serializers.CharField(source='country.name', read_only=True)

    class Meta:
        model = Region
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    """Serializer for City model"""
    region_name = serializers.CharField(source='region.name', read_only=True)
    country_name = serializers.CharField(source='region.country.name', read_only=True)

    class Meta:
        model = City
        fields = '__all__'


class DistrictSerializer(serializers.ModelSerializer):
    """Serializer for District model"""
    city_name = serializers.CharField(source='city.name', read_only=True)
    region_name = serializers.CharField(source='city.region.name', read_only=True)

    class Meta:
        model = District
        fields = '__all__'


class ChannelSerializer(serializers.ModelSerializer):
    """Serializer for Channel model"""
    district_name = serializers.CharField(source='district.name', read_only=True, allow_null=True)
    city_name = serializers.CharField(source='district.city.name', read_only=True, allow_null=True)

    class Meta:
        model = Channel
        fields = '__all__'


class OutletSerializer(serializers.ModelSerializer):
    """Serializer for Outlet model"""
    channel_name = serializers.CharField(source='channel.name', read_only=True)

    class Meta:
        model = Outlet
        fields = '__all__'


class FootfallCounterSerializer(serializers.ModelSerializer):
    """Serializer for FootfallCounter model"""
    outlet_name = serializers.CharField(source='outlet.name', read_only=True)

    class Meta:
        model = FootfallCounter
        fields = '__all__'


class OutletInventorySerializer(serializers.ModelSerializer):
    """Serializer for OutletInventory model"""
    outlet_name = serializers.CharField(source='outlet.name', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = OutletInventory
        fields = '__all__'


class DisplaySerializer(serializers.ModelSerializer):
    """Serializer for Display model"""
    outlet_name = serializers.CharField(source='outlet.name', read_only=True)

    class Meta:
        model = Display
        fields = '__all__'


class DisplayInventorySerializer(serializers.ModelSerializer):
    """Serializer for DisplayInventory model"""
    display_name = serializers.CharField(source='display.name', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = DisplayInventory
        fields = '__all__'
