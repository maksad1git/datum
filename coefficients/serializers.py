"""
DRF Serializers for COEFFICIENTS app models
"""
from rest_framework import serializers
from .models import Coefficient, Metric, Formula, Rule


class CoefficientSerializer(serializers.ModelSerializer):
    """Serializer for Coefficient model"""
    value_type_display = serializers.CharField(source='get_value_type_display', read_only=True)
    
    class Meta:
        model = Coefficient
        fields = '__all__'


class MetricSerializer(serializers.ModelSerializer):
    """Serializer for Metric model"""
    aggregation_type_display = serializers.CharField(source='get_aggregation_type_display', read_only=True)
    
    class Meta:
        model = Metric
        fields = '__all__'


class FormulaSerializer(serializers.ModelSerializer):
    """Serializer for Formula model"""
    
    class Meta:
        model = Formula
        fields = '__all__'


class RuleSerializer(serializers.ModelSerializer):
    """Serializer for Rule model"""
    condition_type_display = serializers.CharField(source='get_condition_type_display', read_only=True)
    
    class Meta:
        model = Rule
        fields = '__all__'
