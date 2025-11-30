from django import forms
from .models import Dashboard, Report, ReportTemplate, FilterPreset


class DashboardForm(forms.ModelForm):
    """Form for Dashboard model"""

    class Meta:
        model = Dashboard
        fields = ['name', 'code', 'description', 'dashboard_type', 'widgets_config', 'default_filters', 'refresh_interval', 'is_public', 'shared_with', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название дашборда'
            }),
            'code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите код дашборда'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Описание дашборда'
            }),
            'dashboard_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'widgets_config': forms.HiddenInput(),
            'default_filters': forms.HiddenInput(),
            'refresh_interval': forms.HiddenInput(),
            'is_public': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'shared_with': forms.SelectMultiple(attrs={
                'class': 'form-select',
                'size': '5'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


class ReportForm(forms.ModelForm):
    """Form for Report model"""

    class Meta:
        model = Report
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название отчета'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Описание отчета'
            }),
            'template': forms.Select(attrs={
                'class': 'form-select'
            }),
            'created_by': forms.Select(attrs={
                'class': 'form-select'
            }),
            'date_from': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'date_to': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'filters': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': '{"key": "value"}'
            }),
            'data': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': '{"results": []}'
            }),
            'format': forms.Select(attrs={
                'class': 'form-select'
            }),
            'file': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'generated_at': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'generation_time': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Время генерации в секундах',
                'step': '0.01'
            }),
        }


class ReportTemplateForm(forms.ModelForm):
    """Form for ReportTemplate model"""

    class Meta:
        model = ReportTemplate
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название шаблона отчета'
            }),
            'code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите код шаблона'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Описание шаблона отчета'
            }),
            'report_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'config': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 8,
                'placeholder': '{"structure": {}, "parameters": {}}'
            }),
            'sql_query': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 8,
                'placeholder': 'SELECT * FROM table WHERE ...'
            }),
            'metrics': forms.CheckboxSelectMultiple(attrs={
                'class': 'form-check-input'
            }),
            'created_by': forms.Select(attrs={
                'class': 'form-select'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


class FilterPresetForm(forms.ModelForm):
    """Form for FilterPreset model"""

    class Meta:
        model = FilterPreset
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название набора фильтров'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Описание набора фильтров'
            }),
            'owner': forms.Select(attrs={
                'class': 'form-select'
            }),
            'applies_to': forms.Select(attrs={
                'class': 'form-select'
            }),
            'filters': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 8,
                'placeholder': '{"date_from": "2024-01-01", "countries": [1, 2], "brands": [10, 11]}'
            }),
            'is_public': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
