"""
Multi-level validation system for Datum
Provides ERROR, WARNING, and INFO level validation messages
"""
from typing import List, Dict, Any, Tuple, Optional
from datetime import datetime, date
from decimal import Decimal
from django.utils.translation import gettext as _


class ValidationLevel:
    """Validation message levels"""
    ERROR = 'error'      # Critical - prevent save
    WARNING = 'warning'  # Warning - allow save but show warning
    INFO = 'info'        # Information - just inform user


class ValidationMessage:
    """A single validation message"""

    def __init__(self, level: str, field: str, message: str, code: str = None):
        self.level = level
        self.field = field
        self.message = message
        self.code = code or f"{level}_{field}"

    def __repr__(self):
        return f"<ValidationMessage {self.level.upper()}: {self.field} - {self.message}>"

    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            'level': self.level,
            'field': self.field,
            'message': self.message,
            'code': self.code
        }


class BaseValidator:
    """Base validator with common validation methods"""

    def __init__(self):
        self.messages: List[ValidationMessage] = []

    def add_error(self, field: str, message: str, code: str = None):
        """Add ERROR level message"""
        self.messages.append(ValidationMessage(ValidationLevel.ERROR, field, message, code))

    def add_warning(self, field: str, message: str, code: str = None):
        """Add WARNING level message"""
        self.messages.append(ValidationMessage(ValidationLevel.WARNING, field, message, code))

    def add_info(self, field: str, message: str, code: str = None):
        """Add INFO level message"""
        self.messages.append(ValidationMessage(ValidationLevel.INFO, field, message, code))

    def has_errors(self) -> bool:
        """Check if there are any ERROR level messages"""
        return any(msg.level == ValidationLevel.ERROR for msg in self.messages)

    def get_messages(self) -> List[ValidationMessage]:
        """Get all validation messages"""
        return self.messages

    def get_errors(self) -> List[ValidationMessage]:
        """Get only ERROR level messages"""
        return [msg for msg in self.messages if msg.level == ValidationLevel.ERROR]

    def get_warnings(self) -> List[ValidationMessage]:
        """Get only WARNING level messages"""
        return [msg for msg in self.messages if msg.level == ValidationLevel.WARNING]

    def clear_messages(self):
        """Clear all messages"""
        self.messages = []

    # =========================================================================
    # COMMON VALIDATION METHODS
    # =========================================================================

    def validate_required(self, field_name: str, value: Any, display_name: str = None):
        """Validate that a field is not empty"""
        display_name = display_name or field_name
        if value is None or value == '' or (isinstance(value, str) and not value.strip()):
            self.add_error(field_name, f"Поле '{display_name}' обязательно для заполнения")

    def validate_positive(self, field_name: str, value: Any, display_name: str = None):
        """Validate that a numeric field is positive"""
        display_name = display_name or field_name
        if value is not None:
            try:
                num_value = float(value) if not isinstance(value, (int, float, Decimal)) else value
                if num_value < 0:
                    self.add_error(field_name, f"Поле '{display_name}' не может быть отрицательным")
            except (ValueError, TypeError):
                self.add_error(field_name, f"Поле '{display_name}' должно быть числом")

    def validate_range(self, field_name: str, value: Any, min_val: float = None, max_val: float = None, display_name: str = None):
        """Validate that a value is within a range"""
        display_name = display_name or field_name
        if value is not None:
            try:
                num_value = float(value) if not isinstance(value, (int, float, Decimal)) else value
                if min_val is not None and num_value < min_val:
                    self.add_error(field_name, f"Поле '{display_name}' не может быть меньше {min_val}")
                if max_val is not None and num_value > max_val:
                    self.add_error(field_name, f"Поле '{display_name}' не может быть больше {max_val}")
            except (ValueError, TypeError):
                self.add_error(field_name, f"Поле '{display_name}' должно быть числом")

    def validate_percentage(self, field_name: str, value: Any, display_name: str = None):
        """Validate that a value is a valid percentage (0-100)"""
        self.validate_range(field_name, value, min_val=0, max_val=100, display_name=display_name)

    def validate_date_not_future(self, field_name: str, value: Any, display_name: str = None):
        """Validate that a date is not in the future"""
        display_name = display_name or field_name
        if value:
            check_date = value.date() if isinstance(value, datetime) else value
            if check_date > date.today():
                self.add_error(field_name, f"Поле '{display_name}' не может быть в будущем")

    def validate_date_range(self, start_field: str, end_field: str, start_value: Any, end_value: Any):
        """Validate that start date is before end date"""
        if start_value and end_value:
            start_date = start_value if isinstance(start_value, (date, datetime)) else None
            end_date = end_value if isinstance(end_value, (date, datetime)) else None

            if start_date and end_date:
                if start_date > end_date:
                    self.add_error(end_field, "Дата окончания не может быть раньше даты начала")

    def validate_gps_coordinates(self, lat_field: str, lon_field: str, lat_value: Any, lon_value: Any):
        """Validate GPS coordinates"""
        if lat_value is not None:
            try:
                lat = float(lat_value)
                if lat < -90 or lat > 90:
                    self.add_error(lat_field, "Широта должна быть в диапазоне от -90 до 90")
            except (ValueError, TypeError):
                self.add_error(lat_field, "Широта должна быть числом")

        if lon_value is not None:
            try:
                lon = float(lon_value)
                if lon < -180 or lon > 180:
                    self.add_error(lon_field, "Долгота должна быть в диапазоне от -180 до 180")
            except (ValueError, TypeError):
                self.add_error(lon_field, "Долгота должна быть числом")


class VisitValidator(BaseValidator):
    """Validator for Visit model"""

    def validate(self, visit) -> Tuple[bool, List[ValidationMessage]]:
        """
        Validate a visit instance
        Returns: (is_valid, messages)
        """
        self.clear_messages()

        # Required fields
        self.validate_required('visit_type', visit.visit_type, 'Тип визита')
        self.validate_required('outlet', visit.outlet, 'Торговая точка')
        self.validate_required('user', visit.user, 'Пользователь')

        # Date validations
        if visit.planned_date:
            # Warning if planned date is in the past
            if visit.planned_date.date() < date.today():
                self.add_warning('planned_date', 'Планируемая дата визита в прошлом')

        # Date range validation
        self.validate_date_range('start_date', 'end_date', visit.start_date, visit.end_date)

        # Start date should not be in the future for completed visits
        if visit.status == 'completed' and visit.start_date:
            self.validate_date_not_future('start_date', visit.start_date, 'Дата начала')

        # GPS coordinates validation
        if visit.latitude is not None or visit.longitude is not None:
            self.validate_gps_coordinates('latitude', 'longitude', visit.latitude, visit.longitude)

            # Warning if GPS is missing for a visit type that requires it
            if hasattr(visit.visit_type, 'requires_gps') and visit.visit_type.requires_gps:
                if visit.latitude is None or visit.longitude is None:
                    self.add_warning('latitude', 'Координаты GPS обязательны для этого типа визита')

        # Status validations
        if visit.status == 'completed':
            if not visit.end_date:
                self.add_warning('end_date', 'Завершенный визит должен иметь дату окончания')

        if visit.status == 'in_progress':
            if not visit.start_date:
                self.add_warning('start_date', 'Визит в процессе должен иметь дату начала')

        return not self.has_errors(), self.get_messages()


class ObservationValidator(BaseValidator):
    """Validator for Observation model"""

    def validate(self, observation) -> Tuple[bool, List[ValidationMessage]]:
        """
        Validate an observation instance
        Returns: (is_valid, messages)
        """
        self.clear_messages()

        # Required fields
        self.validate_required('visit', observation.visit, 'Визит')
        self.validate_required('coefficient', observation.coefficient, 'Коэффициент')

        # At least one value should be provided
        has_value = any([
            observation.value_numeric is not None,
            observation.value_text,
            observation.value_boolean is not None
        ])

        if not has_value:
            self.add_error('value_numeric', 'Должно быть заполнено хотя бы одно поле значения')

        # Numeric value validations
        if observation.value_numeric is not None:
            # Check if coefficient has expected range
            if hasattr(observation.coefficient, 'min_value') and observation.coefficient.min_value is not None:
                if observation.value_numeric < observation.coefficient.min_value:
                    self.add_error('value_numeric',
                                 f"Значение не может быть меньше {observation.coefficient.min_value}")

            if hasattr(observation.coefficient, 'max_value') and observation.coefficient.max_value is not None:
                if observation.value_numeric > observation.coefficient.max_value:
                    self.add_error('value_numeric',
                                 f"Значение не может быть больше {observation.coefficient.max_value}")

            # Warning for unusual values
            if observation.value_numeric == 0:
                self.add_warning('value_numeric', 'Значение равно нулю - проверьте корректность')

        # Product validation
        if observation.product:
            # Info: product is specified
            self.add_info('product', f'Наблюдение связано с продуктом: {observation.product.name}')

        return not self.has_errors(), self.get_messages()


class OutletValidator(BaseValidator):
    """Validator for Outlet model"""

    def validate(self, outlet) -> Tuple[bool, List[ValidationMessage]]:
        """
        Validate an outlet instance
        Returns: (is_valid, messages)
        """
        self.clear_messages()

        # Required fields
        self.validate_required('name', outlet.name, 'Название')
        self.validate_required('channel', outlet.channel, 'Канал сбыта')

        # GPS coordinates
        if outlet.latitude is not None or outlet.longitude is not None:
            self.validate_gps_coordinates('latitude', 'longitude', outlet.latitude, outlet.longitude)
        else:
            self.add_warning('latitude', 'Рекомендуется указать GPS координаты точки продаж')

        # Contact information
        if not outlet.contact_phone and not outlet.contact_person:
            self.add_warning('contact_phone', 'Рекомендуется указать контактные данные')

        # Address
        if not outlet.address or len(outlet.address.strip()) < 10:
            self.add_warning('address', 'Рекомендуется указать полный адрес точки продаж')

        # Status
        if outlet.status == 'inactive':
            self.add_info('status', 'Точка продаж неактивна')

        return not self.has_errors(), self.get_messages()


class ProductValidator(BaseValidator):
    """Validator for Product model"""

    def validate(self, product) -> Tuple[bool, List[ValidationMessage]]:
        """
        Validate a product instance
        Returns: (is_valid, messages)
        """
        self.clear_messages()

        # Required fields
        self.validate_required('name', product.name, 'Название')
        self.validate_required('brand', product.brand, 'Бренд')
        self.validate_required('category', product.category, 'Категория')

        # SKU validation
        if not product.sku:
            self.add_warning('sku', 'Рекомендуется указать артикул (SKU)')

        # Price validation
        if product.price is not None:
            self.validate_positive('price', product.price, 'Цена')

            if product.price == 0:
                self.add_warning('price', 'Цена равна нулю')
        else:
            self.add_warning('price', 'Рекомендуется указать цену')

        # Weight validation
        if product.weight is not None:
            self.validate_positive('weight', product.weight, 'Вес')

        # Status
        if product.status == 'discontinued':
            self.add_info('status', 'Продукт снят с производства')

        return not self.has_errors(), self.get_messages()


class BatchValidator:
    """Validator for batch operations"""

    @staticmethod
    def validate_sum_to_hundred(values: Dict[str, float], field_name: str = 'values') -> Tuple[bool, List[ValidationMessage]]:
        """
        Validate that a set of percentages sum to 100%
        Used for market share, distribution percentages, etc.
        """
        messages = []
        total = sum(values.values())

        if abs(total - 100) > 0.01:  # Allow small floating point errors
            messages.append(ValidationMessage(
                ValidationLevel.ERROR,
                field_name,
                f"Сумма процентов должна быть равна 100% (текущая сумма: {total:.2f}%)"
            ))

        has_errors = any(msg.level == ValidationLevel.ERROR for msg in messages)
        return not has_errors, messages

    @staticmethod
    def validate_unique_codes(items: List[Any], code_field: str = 'code') -> Tuple[bool, List[ValidationMessage]]:
        """Validate that codes are unique in a batch"""
        messages = []
        codes = {}

        for idx, item in enumerate(items):
            code = getattr(item, code_field, None) if hasattr(item, code_field) else item.get(code_field)

            if code in codes:
                messages.append(ValidationMessage(
                    ValidationLevel.ERROR,
                    code_field,
                    f"Код '{code}' дублируется (строки {codes[code] + 1} и {idx + 1})"
                ))
            else:
                codes[code] = idx

        has_errors = any(msg.level == ValidationLevel.ERROR for msg in messages)
        return not has_errors, messages
