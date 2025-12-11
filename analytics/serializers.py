"""
DRF Serializers for ANALYTICS app models
"""
from rest_framework import serializers
from .models import Dashboard, Report, ReportTemplate, FilterPreset, ForecastModel


class DashboardSerializer(serializers.ModelSerializer):
    """Serializer for Dashboard model"""
    owner_name = serializers.CharField(source='owner.username', read_only=True)
    dashboard_type_display = serializers.CharField(source='get_dashboard_type_display', read_only=True)
    level_display = serializers.CharField(source='get_level_display', read_only=True, allow_null=True)
    shared_with_count = serializers.SerializerMethodField()

    class Meta:
        model = Dashboard
        fields = '__all__'

    def get_shared_with_count(self, obj):
        return obj.shared_with.count()


class ReportSerializer(serializers.ModelSerializer):
    """Serializer for Report model"""
    template_name = serializers.CharField(source='template.name', read_only=True, allow_null=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    format_display = serializers.CharField(source='get_format_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = Report
        fields = '__all__'

    def get_file_url(self, obj):
        if obj.file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.file.url)
        return None


class ReportTemplateSerializer(serializers.ModelSerializer):
    """Serializer for ReportTemplate model"""
    report_type_display = serializers.CharField(source='get_report_type_display', read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True, allow_null=True)
    metric_count = serializers.SerializerMethodField()
    report_count = serializers.SerializerMethodField()

    class Meta:
        model = ReportTemplate
        fields = '__all__'

    def get_metric_count(self, obj):
        return obj.metrics.count()

    def get_report_count(self, obj):
        return obj.reports.count()


class FilterPresetSerializer(serializers.ModelSerializer):
    """Serializer for FilterPreset model"""
    owner_name = serializers.CharField(source='owner.username', read_only=True)
    applies_to_display = serializers.CharField(source='get_applies_to_display', read_only=True)

    class Meta:
        model = FilterPreset
        fields = '__all__'


class ForecastModelSerializer(serializers.ModelSerializer):
    """Serializer for ForecastModel model"""
    model_type_display = serializers.CharField(source='get_model_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True, allow_null=True)
    metric_count = serializers.SerializerMethodField()

    class Meta:
        model = ForecastModel
        fields = '__all__'

    def get_metric_count(self, obj):
        return obj.metrics.count()
