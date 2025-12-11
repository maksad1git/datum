"""
DRF Serializers for VISITS app models
"""
from rest_framework import serializers
from .models import VisitType, Visit, Observation, VisitMedia, Sale


class VisitTypeSerializer(serializers.ModelSerializer):
    """Serializer for VisitType model"""
    form_template_name = serializers.CharField(source='form_template.name', read_only=True, allow_null=True)
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    coefficient_count = serializers.SerializerMethodField()

    class Meta:
        model = VisitType
        fields = '__all__'

    def get_coefficient_count(self, obj):
        return obj.coefficients.count()


class VisitSerializer(serializers.ModelSerializer):
    """Serializer for Visit model"""
    visit_type_name = serializers.CharField(source='visit_type.name', read_only=True)
    outlet_name = serializers.CharField(source='outlet.name', read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    data_source_type_display = serializers.CharField(source='get_data_source_type_display', read_only=True)
    observation_count = serializers.SerializerMethodField()
    media_count = serializers.SerializerMethodField()

    class Meta:
        model = Visit
        fields = '__all__'

    def get_observation_count(self, obj):
        return obj.observations.count()

    def get_media_count(self, obj):
        return obj.media.count()


class ObservationSerializer(serializers.ModelSerializer):
    """Serializer for Observation model"""
    visit_info = serializers.SerializerMethodField()
    coefficient_name = serializers.CharField(source='coefficient.name', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True, allow_null=True)
    data_source_type_display = serializers.CharField(source='get_data_source_type_display', read_only=True)
    value = serializers.SerializerMethodField()

    class Meta:
        model = Observation
        fields = '__all__'

    def get_visit_info(self, obj):
        return f"{obj.visit.visit_type.name} - {obj.visit.outlet.name}"

    def get_value(self, obj):
        return obj.get_value()


class VisitMediaSerializer(serializers.ModelSerializer):
    """Serializer for VisitMedia model"""
    visit_info = serializers.SerializerMethodField()
    observation_info = serializers.SerializerMethodField()
    media_type_display = serializers.CharField(source='get_media_type_display', read_only=True)
    file_url = serializers.SerializerMethodField()
    thumbnail_url = serializers.SerializerMethodField()

    class Meta:
        model = VisitMedia
        fields = '__all__'

    def get_visit_info(self, obj):
        return f"{obj.visit.visit_type.name} - {obj.visit.outlet.name}"

    def get_observation_info(self, obj):
        if obj.observation:
            return f"{obj.observation.coefficient.name}"
        return None

    def get_file_url(self, obj):
        if obj.file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.file.url)
        return None

    def get_thumbnail_url(self, obj):
        if obj.thumbnail:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.thumbnail.url)
        return None


class SaleSerializer(serializers.ModelSerializer):
    """Serializer for Sale model"""
    outlet_name = serializers.CharField(source='outlet.name', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)
    recorded_by_username = serializers.CharField(source='recorded_by.username', read_only=True, allow_null=True)

    class Meta:
        model = Sale
        fields = '__all__'
        read_only_fields = ['total_amount', 'recorded_at']
