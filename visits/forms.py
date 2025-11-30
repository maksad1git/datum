from django import forms
from .models import VisitType, Visit, Observation, VisitMedia


class VisitTypeForm(forms.ModelForm):
    """Form for VisitType model"""

    class Meta:
        model = VisitType
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название типа визита'
            }),
            'code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите код типа визита'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Описание типа визита'
            }),
            'form_template': forms.Select(attrs={
                'class': 'form-select'
            }),
            'coefficients': forms.CheckboxSelectMultiple(attrs={
                'class': 'form-check-input'
            }),
            'type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'requires_photo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'requires_signature': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'requires_gps': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'settings': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': '{"key": "value"}'
            }),
        }


class VisitForm(forms.ModelForm):
    """Form for Visit model with cascading dropdowns support"""

    class Meta:
        model = Visit
        fields = '__all__'
        widgets = {
            'visit_type': forms.Select(attrs={
                'class': 'form-select select2'
            }),
            'outlet': forms.Select(attrs={
                'class': 'form-select select2',
                'id': 'id_outlet'
            }),
            'user': forms.Select(attrs={
                'class': 'form-select select2'
            }),
            'planned_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'start_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'end_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'latitude': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '55.7558',
                'step': '0.000001'
            }),
            'longitude': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '37.6173',
                'step': '0.000001'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Комментарии по визиту'
            }),
            'form_data': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': '{"key": "value"}'
            }),
            'signature': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'data_source_type': forms.RadioSelect(attrs={
                'class': 'form-check-input'
            }),
        }


class ObservationForm(forms.ModelForm):
    """Form for Observation model with cascading dropdowns support"""

    class Meta:
        model = Observation
        fields = '__all__'
        widgets = {
            'visit': forms.Select(attrs={
                'class': 'form-select select2'
            }),
            'coefficient': forms.Select(attrs={
                'class': 'form-select select2'
            }),
            'product': forms.Select(attrs={
                'class': 'form-select select2',
                'id': 'id_product'
            }),
            'value_numeric': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Числовое значение',
                'step': '0.0001'
            }),
            'value_text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Текстовое значение'
            }),
            'value_boolean': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Комментарии'
            }),
            'metadata': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': '{"key": "value"}'
            }),
            'data_source_type': forms.RadioSelect(attrs={
                'class': 'form-check-input'
            }),
        }


class VisitMediaForm(forms.ModelForm):
    """Form for VisitMedia model"""

    class Meta:
        model = VisitMedia
        fields = '__all__'
        widgets = {
            'visit': forms.Select(attrs={
                'class': 'form-select'
            }),
            'observation': forms.Select(attrs={
                'class': 'form-select'
            }),
            'media_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'file': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'thumbnail': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название файла'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Описание медиа файла'
            }),
            'exif_data': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': '{"key": "value"}'
            }),
            'latitude': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '55.7558',
                'step': '0.000001'
            }),
            'longitude': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '37.6173',
                'step': '0.000001'
            }),
        }
