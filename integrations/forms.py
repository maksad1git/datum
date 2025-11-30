from django import forms
from .models import ImportJob, ExportJob, Backup


class ImportJobForm(forms.ModelForm):
    """Form for ImportJob model"""

    class Meta:
        model = ImportJob
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название задания импорта'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Описание задания импорта'
            }),
            'created_by': forms.Select(attrs={
                'class': 'form-select'
            }),
            'source_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'source_file': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'source_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com/data.csv'
            }),
            'data_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'data_format': forms.Select(attrs={
                'class': 'form-select'
            }),
            'mapping': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': '{"source_field": "target_field", "name": "name"}'
            }),
            'options': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': '{"skip_duplicates": true, "update_existing": false}'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'total_records': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'imported_records': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'failed_records': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'skipped_records': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'error_log': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Лог ошибок импорта'
            }),
            'error_file': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'started_at': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'completed_at': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'duration': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Длительность в секундах',
                'step': '0.01'
            }),
        }


class ExportJobForm(forms.ModelForm):
    """Form for ExportJob model"""

    class Meta:
        model = ExportJob
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название задания экспорта'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Описание задания экспорта'
            }),
            'created_by': forms.Select(attrs={
                'class': 'form-select'
            }),
            'data_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'export_format': forms.Select(attrs={
                'class': 'form-select'
            }),
            'filters': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': '{"date_from": "2024-01-01", "status": "active"}'
            }),
            'options': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': '{"include_headers": true, "delimiter": ","}'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'file': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'total_records': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'file_size': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': 'Размер в байтах'
            }),
            'error_log': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Лог ошибок экспорта'
            }),
            'started_at': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'completed_at': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'duration': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Длительность в секундах',
                'step': '0.01'
            }),
            'expires_at': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
        }


class BackupForm(forms.ModelForm):
    """Form for Backup model"""

    class Meta:
        model = Backup
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название резервной копии'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Описание резервной копии'
            }),
            'created_by': forms.Select(attrs={
                'class': 'form-select'
            }),
            'backup_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'includes_database': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'includes_media': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'includes_settings': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'file': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'file_size': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': 'Размер в байтах'
            }),
            'checksum': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'SHA256 контрольная сумма'
            }),
            'metadata': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': '{"tables": [], "version": "1.0"}'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'started_at': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'completed_at': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'duration': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Длительность в секундах',
                'step': '0.01'
            }),
            'expires_at': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'is_restored': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'restored_at': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'restored_by': forms.Select(attrs={
                'class': 'form-select'
            }),
            'error_log': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Лог ошибок резервного копирования'
            }),
        }
