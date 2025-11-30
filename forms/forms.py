from django import forms
from .models import FormTemplate


class FormTemplateForm(forms.ModelForm):
    """Form for FormTemplate model"""

    class Meta:
        model = FormTemplate
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название шаблона формы'
            }),
            'code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите код шаблона'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Описание шаблона формы'
            }),
            'form_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'fields_schema': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10,
                'placeholder': '[{"field_name": "example", "field_type": "text", "label": "Example", "required": true}]'
            }),
            'category': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Категория формы'
            }),
            'version': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '1.0'
            }),
            'parent_version': forms.Select(attrs={
                'class': 'form-select'
            }),
            'applies_to_channels': forms.CheckboxSelectMultiple(attrs={
                'class': 'form-check-input'
            }),
            'created_by': forms.Select(attrs={
                'class': 'form-select'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'settings': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': '{"key": "value"}'
            }),
        }
