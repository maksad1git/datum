from django import forms
from .models import (
    Brand, Category, Product,
    AttributeGroup, AttributeDefinition,
    ProductAttributeValue, CategoryAttributeTemplate
)


class BrandForm(forms.ModelForm):
    """Form for Brand model"""

    class Meta:
        model = Brand
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название бренда'
            }),
            'code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите код бренда'
            }),
            'logo': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Описание бренда'
            }),
            'country': forms.Select(attrs={
                'class': 'form-select'
            }),
            'settings': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': '{"key": "value"}'
            }),
        }


class CategoryForm(forms.ModelForm):
    """Form for Category model"""

    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название категории'
            }),
            'code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите код категории'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Описание категории'
            }),
            'parent': forms.Select(attrs={
                'class': 'form-select'
            }),
            'settings': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': '{"key": "value"}'
            }),
        }


class ProductForm(forms.ModelForm):
    """Form for Product model with cascading dropdowns support"""

    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название товара'
            }),
            'sku_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите артикул (SKU)'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Описание товара'
            }),
            'brand': forms.Select(attrs={
                'class': 'form-select select2',
                'id': 'id_brand'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select select2',
                'id': 'id_category'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'weight': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Вес в граммах',
                'step': '0.001'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Цена',
                'step': '0.01'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'attributes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': '{"color": "red", "size": "large"}'
            }),
        }


# ============================================================================
# EAV SYSTEM FORMS
# ============================================================================

class AttributeGroupForm(forms.ModelForm):
    """Форма для создания групп атрибутов"""

    class Meta:
        model = AttributeGroup
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Например: Металл, Камни, Размеры'
            }),
            'code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'metal, stones, sizes'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select select2',
                'id': 'id_category'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


class AttributeDefinitionForm(forms.ModelForm):
    """Форма для создания определений атрибутов"""

    class Meta:
        model = AttributeDefinition
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Например: Проба металла, Тип камня'
            }),
            'code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'metal_purity, stone_type'
            }),
            'group': forms.Select(attrs={
                'class': 'form-select select2'
            }),
            'data_type': forms.Select(attrs={
                'class': 'form-select',
                'onchange': 'toggleAttributeFields(this.value)'
            }),
            'is_required': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'is_filterable': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'is_searchable': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'min_value': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Минимальное значение',
                'step': '0.01'
            }),
            'max_value': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Максимальное значение',
                'step': '0.01'
            }),
            'max_length': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '255'
            }),
            'choices': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': '["Золото", "Серебро", "Платина"]'
            }),
            'unit': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'г, мм, карат, см'
            }),
            'placeholder': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите значение...'
            }),
            'help_text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Подсказка для пользователя'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


class ProductAttributeValueForm(forms.ModelForm):
    """Форма для установки значений атрибутов товара"""

    class Meta:
        model = ProductAttributeValue
        fields = '__all__'
        widgets = {
            'product': forms.Select(attrs={
                'class': 'form-select select2'
            }),
            'attribute': forms.Select(attrs={
                'class': 'form-select select2',
                'onchange': 'updateAttributeFields(this)'
            }),
            'value_text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Текстовое значение'
            }),
            'value_integer': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Целое число'
            }),
            'value_decimal': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Десятичное число',
                'step': '0.0001'
            }),
            'value_boolean': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'value_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'value_choice': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Выбранное значение'
            }),
            'value_multi_choice': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': '["Значение 1", "Значение 2"]'
            }),
            'value_file': forms.FileInput(attrs={
                'class': 'form-control'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Если есть instance, показываем только релевантное поле значения
        if self.instance and self.instance.pk:
            try:
                if self.instance.attribute:
                    attr_type = self.instance.attribute.data_type
                    # Скрываем все поля значений
                    for field in ['value_text', 'value_integer', 'value_decimal',
                                 'value_boolean', 'value_date', 'value_choice',
                                 'value_multi_choice', 'value_file']:
                        if f'value_{attr_type}' != field:
                            self.fields[field].widget = forms.HiddenInput()
            except AttributeDefinition.DoesNotExist:
                # Если атрибут не существует, ничего не скрываем
                pass


class CategoryAttributeTemplateForm(forms.ModelForm):
    """Форма для настройки шаблонов атрибутов категории"""

    class Meta:
        model = CategoryAttributeTemplate
        fields = '__all__'
        widgets = {
            'category': forms.Select(attrs={
                'class': 'form-select select2'
            }),
            'attribute': forms.Select(attrs={
                'class': 'form-select select2'
            }),
            'is_required': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0'
            }),
        }


# ============================================================================
# DYNAMIC ATTRIBUTE FORMSET
# ============================================================================

from django.forms import inlineformset_factory

ProductAttributeValueFormSet = inlineformset_factory(
    Product,
    ProductAttributeValue,
    form=ProductAttributeValueForm,
    extra=3,
    can_delete=True,
    fields=['attribute', 'value_text', 'value_integer', 'value_decimal',
            'value_boolean', 'value_date', 'value_choice', 'value_multi_choice', 'value_file']
)
