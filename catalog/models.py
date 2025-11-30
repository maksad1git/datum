from django.db import models


class Brand(models.Model):
    """Бренд / Производитель"""
    name = models.CharField('Название', max_length=255)
    code = models.CharField('Код', max_length=50, unique=True, blank=True)
    logo = models.ImageField('Логотип', upload_to='brands/', blank=True, null=True)
    description = models.TextField('Описание', blank=True)

    country = models.ForeignKey(
        'geo.Country',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Страна производства',
        related_name='brands'
    )

    # Дополнительные параметры
    settings = models.JSONField('Дополнительные настройки', default=dict, blank=True)

    # Метаданные
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'
        ordering = ['name']

    def __str__(self):
        return self.name


class Category(models.Model):
    """Категория товаров"""
    name = models.CharField('Название', max_length=255)
    code = models.CharField('Код', max_length=50, blank=True)
    description = models.TextField('Описание', blank=True)

    # Иерархия категорий
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Родительская категория',
        related_name='subcategories'
    )

    # Дополнительные параметры
    settings = models.JSONField('Дополнительные настройки', default=dict, blank=True)

    # Метаданные
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        if self.parent:
            return f"{self.parent.name} → {self.name}"
        return self.name


class Product(models.Model):
    """Товар / SKU"""
    name = models.CharField('Название', max_length=255)
    sku_code = models.CharField('Артикул (SKU)', max_length=100, unique=True, blank=True)
    description = models.TextField('Описание', blank=True)

    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
        verbose_name='Бренд',
        related_name='products'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='Категория',
        related_name='products'
    )

    # Характеристики
    image = models.ImageField('Изображение', upload_to='products/', blank=True, null=True)
    weight = models.DecimalField('Вес', max_digits=10, decimal_places=3, null=True, blank=True, help_text='В граммах')
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2, null=True, blank=True)

    # Статус
    STATUS_ACTIVE = 'active'
    STATUS_DISCONTINUED = 'discontinued'
    STATUS_DRAFT = 'draft'
    STATUS_CHOICES = [
        (STATUS_ACTIVE, 'Активен'),
        (STATUS_DISCONTINUED, 'Снят с производства'),
        (STATUS_DRAFT, 'Черновик'),
    ]
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default=STATUS_ACTIVE)

    # Дополнительные параметры
    attributes = models.JSONField('Атрибуты', default=dict, blank=True, help_text='Динамические характеристики товара')

    # Метаданные
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['brand', 'category', 'name']

    def __str__(self):
        return f"{self.brand.name} - {self.name}"


# ============================================================================
# EAV (Entity-Attribute-Value) SYSTEM FOR DYNAMIC ATTRIBUTES
# ============================================================================

class AttributeGroup(models.Model):
    """
    Группа атрибутов (для организации)
    Например: "Металл", "Камни", "Размеры"
    """
    name = models.CharField('Название группы', max_length=200)
    code = models.SlugField('Код группы', max_length=100, unique=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='attribute_groups',
        verbose_name='Категория',
        help_text='К какой категории относится эта группа атрибутов'
    )
    order = models.PositiveIntegerField('Порядок отображения', default=0)
    is_active = models.BooleanField('Активна', default=True)

    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Группа атрибутов'
        verbose_name_plural = 'Группы атрибутов'
        ordering = ['category', 'order', 'name']

    def __str__(self):
        return f"{self.category.name} / {self.name}"


class AttributeDefinition(models.Model):
    """
    Определение атрибута (шаблон)
    Например: "Проба металла", "Тип камня", "Размер кольца"
    """

    # Типы данных для атрибутов
    TYPE_TEXT = 'text'
    TYPE_INTEGER = 'integer'
    TYPE_DECIMAL = 'decimal'
    TYPE_BOOLEAN = 'boolean'
    TYPE_DATE = 'date'
    TYPE_CHOICE = 'choice'
    TYPE_MULTI_CHOICE = 'multi_choice'
    TYPE_FILE = 'file'

    ATTRIBUTE_TYPES = [
        (TYPE_TEXT, 'Текст'),
        (TYPE_INTEGER, 'Целое число'),
        (TYPE_DECIMAL, 'Десятичное число'),
        (TYPE_BOOLEAN, 'Да/Нет'),
        (TYPE_DATE, 'Дата'),
        (TYPE_CHOICE, 'Выбор из списка'),
        (TYPE_MULTI_CHOICE, 'Множественный выбор'),
        (TYPE_FILE, 'Файл'),
    ]

    # Основные поля
    name = models.CharField('Название атрибута', max_length=200)
    code = models.SlugField('Код атрибута', max_length=100, unique=True)
    group = models.ForeignKey(
        AttributeGroup,
        on_delete=models.CASCADE,
        related_name='attributes',
        verbose_name='Группа',
        null=True,
        blank=True
    )

    # Тип данных
    data_type = models.CharField(
        'Тип данных',
        max_length=20,
        choices=ATTRIBUTE_TYPES,
        default=TYPE_TEXT
    )

    # Настройки валидации
    is_required = models.BooleanField('Обязательный', default=False)
    is_filterable = models.BooleanField('Можно фильтровать', default=True)
    is_searchable = models.BooleanField('Можно искать', default=False)

    # Для числовых типов
    min_value = models.DecimalField(
        'Минимальное значение',
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    max_value = models.DecimalField(
        'Максимальное значение',
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    # Для текстовых типов
    max_length = models.PositiveIntegerField(
        'Максимальная длина',
        null=True,
        blank=True,
        default=255
    )

    # Для выбора из списка
    choices = models.JSONField(
        'Варианты выбора',
        null=True,
        blank=True,
        help_text='JSON список вариантов: ["Вариант 1", "Вариант 2"]'
    )

    # Единица измерения
    unit = models.CharField(
        'Единица измерения',
        max_length=50,
        blank=True,
        help_text='Например: г, мм, карат, см'
    )

    # UI настройки
    placeholder = models.CharField(
        'Плейсхолдер',
        max_length=200,
        blank=True,
        help_text='Подсказка в поле ввода'
    )
    help_text = models.TextField(
        'Текст подсказки',
        blank=True,
        help_text='Подробное описание атрибута'
    )

    # Порядок и активность
    order = models.PositiveIntegerField('Порядок отображения', default=0)
    is_active = models.BooleanField('Активен', default=True)

    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Определение атрибута'
        verbose_name_plural = 'Определения атрибутов'
        ordering = ['group', 'order', 'name']

    def __str__(self):
        unit_str = f" ({self.unit})" if self.unit else ""
        return f"{self.name}{unit_str}"

    def get_choices_list(self):
        """Получить список вариантов для выбора"""
        if self.data_type in [self.TYPE_CHOICE, self.TYPE_MULTI_CHOICE]:
            return self.choices or []
        return []


class ProductAttributeValue(models.Model):
    """
    Значение атрибута для конкретного товара (EAV)
    """
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='attribute_values',
        verbose_name='Товар'
    )
    attribute = models.ForeignKey(
        AttributeDefinition,
        on_delete=models.CASCADE,
        related_name='values',
        verbose_name='Атрибут'
    )

    # Значения для разных типов
    value_text = models.TextField('Текстовое значение', null=True, blank=True)
    value_integer = models.IntegerField('Целочисленное значение', null=True, blank=True)
    value_decimal = models.DecimalField(
        'Десятичное значение',
        max_digits=10,
        decimal_places=4,
        null=True,
        blank=True
    )
    value_boolean = models.BooleanField('Булево значение', null=True, blank=True)
    value_date = models.DateField('Значение даты', null=True, blank=True)
    value_choice = models.CharField('Выбранное значение', max_length=200, null=True, blank=True)
    value_multi_choice = models.JSONField('Множественный выбор', null=True, blank=True)
    value_file = models.FileField('Файл', upload_to='product_attributes/', null=True, blank=True)

    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Значение атрибута'
        verbose_name_plural = 'Значения атрибутов'
        unique_together = ['product', 'attribute']
        ordering = ['product', 'attribute__group', 'attribute__order']

    def __str__(self):
        return f"{self.product.name} / {self.attribute.name} = {self.get_value()}"

    def get_value(self):
        """Получить значение в зависимости от типа"""
        attr_type = self.attribute.data_type

        if attr_type == AttributeDefinition.TYPE_TEXT:
            return self.value_text
        elif attr_type == AttributeDefinition.TYPE_INTEGER:
            return self.value_integer
        elif attr_type == AttributeDefinition.TYPE_DECIMAL:
            return self.value_decimal
        elif attr_type == AttributeDefinition.TYPE_BOOLEAN:
            return 'Да' if self.value_boolean else 'Нет'
        elif attr_type == AttributeDefinition.TYPE_DATE:
            return self.value_date
        elif attr_type == AttributeDefinition.TYPE_CHOICE:
            return self.value_choice
        elif attr_type == AttributeDefinition.TYPE_MULTI_CHOICE:
            return ', '.join(self.value_multi_choice) if self.value_multi_choice else None
        elif attr_type == AttributeDefinition.TYPE_FILE:
            return self.value_file.name if self.value_file else None
        return None

    def set_value(self, value):
        """Установить значение в зависимости от типа"""
        attr_type = self.attribute.data_type

        # Очистить все значения
        self.value_text = None
        self.value_integer = None
        self.value_decimal = None
        self.value_boolean = None
        self.value_date = None
        self.value_choice = None
        self.value_multi_choice = None

        # Установить нужное
        if attr_type == AttributeDefinition.TYPE_TEXT:
            self.value_text = str(value)
        elif attr_type == AttributeDefinition.TYPE_INTEGER:
            self.value_integer = int(value)
        elif attr_type == AttributeDefinition.TYPE_DECIMAL:
            self.value_decimal = float(value)
        elif attr_type == AttributeDefinition.TYPE_BOOLEAN:
            self.value_boolean = bool(value)
        elif attr_type == AttributeDefinition.TYPE_DATE:
            self.value_date = value
        elif attr_type == AttributeDefinition.TYPE_CHOICE:
            self.value_choice = str(value)
        elif attr_type == AttributeDefinition.TYPE_MULTI_CHOICE:
            self.value_multi_choice = value if isinstance(value, list) else [value]


class CategoryAttributeTemplate(models.Model):
    """
    Шаблон атрибутов для категории
    """
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='attribute_templates',
        verbose_name='Категория'
    )
    attribute = models.ForeignKey(
        AttributeDefinition,
        on_delete=models.CASCADE,
        related_name='category_templates',
        verbose_name='Атрибут'
    )
    is_required = models.BooleanField('Обязательный', default=False)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Шаблон атрибута категории'
        verbose_name_plural = 'Шаблоны атрибутов категорий'
        unique_together = ['category', 'attribute']
        ordering = ['category', 'order']

    def __str__(self):
        required = " *" if self.is_required else ""
        return f"{self.category.name} / {self.attribute.name}{required}"
