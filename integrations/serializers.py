from rest_framework import serializers
from .models import ImportJob, ExportJob, Backup

class ImportJobSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    class Meta:
        model = ImportJob
        fields = '__all__'

class ExportJobSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    class Meta:
        model = ExportJob
        fields = '__all__'

class BackupSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    class Meta:
        model = Backup
        fields = '__all__'
