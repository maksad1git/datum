from rest_framework import serializers
from .models import SystemSettings, IntegrationSettings, SystemLog, AuditLog

class SystemSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemSettings
        fields = '__all__'

class IntegrationSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntegrationSettings
        fields = '__all__'

class SystemLogSerializer(serializers.ModelSerializer):
    level_display = serializers.CharField(source='get_level_display', read_only=True)
    class Meta:
        model = SystemLog
        fields = '__all__'

class AuditLogSerializer(serializers.ModelSerializer):
    action_display = serializers.CharField(source='get_action_display', read_only=True)
    class Meta:
        model = AuditLog
        fields = '__all__'
