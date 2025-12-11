from django import forms
from .models import GlobalMarket, Country, Region, City, District, Channel, Outlet


class GlobalMarketForm(forms.ModelForm):
    """Form for GlobalMarket model"""

    class Meta:
        model = GlobalMarket
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название глобального рынка'
            }),
            'code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите код (например, GLOBAL)'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Описание глобального рынка'
            }),
            'currency': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'USD, EUR, RUB и т.д.'
            }),
            'unit_weight': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'kg, g, lb и т.д.'
            }),
            'data_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'settings': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': '{"key": "value"}'
            }),
        }


class CountryForm(forms.ModelForm):
    """Form for Country model with cascading dropdowns support"""

    class Meta:
        model = Country
        fields = '__all__'
        widgets = {
            'global_market': forms.Select(attrs={
                'class': 'form-select select2',
                'id': 'id_global_market'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название страны'
            }),
            'code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите код страны'
            }),
            'iso_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'RUS, USA, DEU и т.д.'
            }),
            'currency': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'RUB, USD, EUR и т.д.'
            }),
            'flag_image': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'settings': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': '{"key": "value"}'
            }),
        }


class RegionForm(forms.ModelForm):
    """Form for Region model with cascading dropdowns support"""

    class Meta:
        model = Region
        fields = '__all__'
        widgets = {
            'country': forms.Select(attrs={
                'class': 'form-select select2',
                'id': 'id_country'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название региона'
            }),
            'code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите код региона'
            }),
            'geo_polygon': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'GeoJSON полигон (необязательно)'
            }),
            'data_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'settings': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': '{"key": "value"}'
            }),
        }


class CityForm(forms.ModelForm):
    """Form for City model with cascading dropdowns support"""

    class Meta:
        model = City
        fields = '__all__'
        widgets = {
            'region': forms.Select(attrs={
                'class': 'form-select select2',
                'id': 'id_region'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название города'
            }),
            'code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите код города'
            }),
            'geo_polygon': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'GeoJSON полигон (необязательно)'
            }),
            'data_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'settings': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': '{"key": "value"}'
            }),
        }


class DistrictForm(forms.ModelForm):
    """Form for District model with cascading dropdowns support"""

    class Meta:
        model = District
        fields = '__all__'
        widgets = {
            'city': forms.Select(attrs={
                'class': 'form-select select2',
                'id': 'id_city'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название района'
            }),
            'code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите код района'
            }),
            'geo_polygon': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'GeoJSON полигон (необязательно)'
            }),
            'data_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'settings': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': '{"key": "value"}'
            }),
        }


class ChannelForm(forms.ModelForm):
    """Form for Channel model with cascading dropdowns support"""

    class Meta:
        model = Channel
        fields = '__all__'
        widgets = {
            'district': forms.Select(attrs={
                'class': 'form-select select2',
                'id': 'id_district'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название канала'
            }),
            'code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите код канала'
            }),
            'type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Описание канала сбыта'
            }),
            'settings': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': '{"key": "value"}'
            }),
        }


class OutletForm(forms.ModelForm):
    """Form for Outlet model with cascading dropdowns support"""

    class Meta:
        model = Outlet
        fields = '__all__'
        widgets = {
            'channel': forms.Select(attrs={
                'class': 'form-select select2',
                'id': 'id_channel'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название точки сбыта'
            }),
            'code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите код точки'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Полный адрес точки сбыта'
            }),
            'contact_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+7 (xxx) xxx-xx-xx'
            }),
            'contact_person': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ФИО контактного лица'
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
            'photo': forms.FileInput(attrs={
                'class': 'form-control'
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
