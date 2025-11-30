from django import forms
from .models import Coefficient, Metric, Formula, Rule


class CoefficientForm(forms.ModelForm):
    """Form for Coefficient model"""

    class Meta:
        model = Coefficient
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название коэффициента'
            }),
            'code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите код коэффициента'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Описание коэффициента'
            }),
            'data_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'applies_to_outlet': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'applies_to_channel': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'applies_to_region': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'applies_to_country': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'applies_to_global': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'value_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'unit': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'штук, кг, % и т.д.'
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


class MetricForm(forms.ModelForm):
    """Form for Metric model"""

    class Meta:
        model = Metric
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название метрики'
            }),
            'code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите код метрики'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Описание метрики'
            }),
            'coefficients': forms.SelectMultiple(attrs={
                'class': 'form-select',
                'size': '8'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'source_data_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'formula': forms.Select(attrs={
                'class': 'form-select'
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем help_text для коэффициентов
        self.fields['coefficients'].help_text = 'Выберите коэффициенты, используемые в этой метрике (можно выбрать несколько)'
        self.fields['coefficients'].required = False


class FormulaForm(forms.ModelForm):
    """Form for Formula model"""

    class Meta:
        model = Formula
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название формулы'
            }),
            'code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите код формулы'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Описание формулы'
            }),
            'source_data_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'expression': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': '(C1 + C2) / C3 * 100'
            }),
            'coefficients': forms.SelectMultiple(attrs={
                'class': 'form-select',
                'size': '8'
            }),
            'result_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'result_unit': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Единица измерения результата'
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['coefficients'].help_text = 'Выберите коэффициенты, используемые в этой формуле (Ctrl+Click для множественного выбора)'
        self.fields['coefficients'].required = False


class RuleForm(forms.ModelForm):
    """Form for Rule model"""

    class Meta:
        model = Rule
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название правила'
            }),
            'code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите код правила'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Описание правила'
            }),
            'rule_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'applies_to': forms.SelectMultiple(attrs={
                'class': 'form-select',
                'size': '8'
            }),
            'aggregation_method': forms.Select(attrs={
                'class': 'form-select'
            }),
            'parameters': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': '{"key": "value"}'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['applies_to'].help_text = 'Выберите коэффициенты, к которым применяется это правило (Ctrl+Click для множественного выбора)'
        self.fields['applies_to'].required = False
