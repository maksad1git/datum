from django.db import models


class GlobalMarket(models.Model):
    """Глобальный рынок (мир)"""
    name = models.CharField('Название', max_length=255)
    code = models.CharField('Код', max_length=50, unique=True)
    description = models.TextField('Описание', blank=True)

    # Настройки
    currency = models.CharField('Валюта', max_length=10, default='USD')
    unit_weight = models.CharField('Единица веса', max_length=20, default='kg')

    # Типы данных
    DATA_EXPERT = 'expert'
    DATA_MONITORING = 'monitoring'
    DATA_MIXED = 'mixed'
    DATA_CHOICES = [
        (DATA_EXPERT, 'Экспертный'),
        (DATA_MONITORING, 'Мониторинговый'),
        (DATA_MIXED, 'Смешанный'),
    ]
    data_type = models.CharField('Тип данных', max_length=20, choices=DATA_CHOICES, default=DATA_MIXED)

    # Дополнительные параметры (JSON для гибкости)
    settings = models.JSONField('Дополнительные настройки', default=dict, blank=True)

    # Метаданные
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Глобальный рынок'
        verbose_name_plural = 'Глобальные рынки'
        ordering = ['name']

    def __str__(self):
        return self.name


class Country(models.Model):
    """Страна"""
    global_market = models.ForeignKey(
        GlobalMarket,
        on_delete=models.CASCADE,
        verbose_name='Глобальный рынок',
        related_name='countries'
    )
    name = models.CharField('Название', max_length=255)
    code = models.CharField('Код', max_length=10, unique=True)
    iso_code = models.CharField('ISO код', max_length=3, unique=True)

    # Параметры
    currency = models.CharField('Валюта', max_length=10)
    flag_image = models.ImageField('Флаг', upload_to='flags/', blank=True, null=True)

    # Дополнительные параметры
    settings = models.JSONField('Дополнительные настройки', default=dict, blank=True)

    # Метаданные
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'
        ordering = ['name']

    def __str__(self):
        return self.name


class Region(models.Model):
    """Регион"""
    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        verbose_name='Страна',
        related_name='regions'
    )
    name = models.CharField('Название', max_length=255)
    code = models.CharField('Код', max_length=50)

    # Геоданные (на потом, пока заглушка)
    geo_polygon = models.JSONField('Полигон (GeoJSON)', null=True, blank=True)

    # Типы данных
    DATA_EXPERT = 'expert'
    DATA_MONITORING = 'monitoring'
    DATA_MIXED = 'mixed'
    DATA_CHOICES = [
        (DATA_EXPERT, 'Экспертный'),
        (DATA_MONITORING, 'Мониторинговый'),
        (DATA_MIXED, 'Смешанный'),
    ]
    data_type = models.CharField('Тип данных', max_length=20, choices=DATA_CHOICES, default=DATA_MIXED)

    # Дополнительные параметры
    settings = models.JSONField('Дополнительные настройки', default=dict, blank=True)

    # Метаданные
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Регион'
        verbose_name_plural = 'Регионы'
        ordering = ['country', 'name']
        unique_together = ['country', 'code']

    def __str__(self):
        return f"{self.country.name} - {self.name}"


class City(models.Model):
    """Город - второй уровень географической иерархии"""
    region = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        verbose_name='Регион',
        related_name='cities'
    )
    name = models.CharField('Название', max_length=255)
    code = models.CharField('Код', max_length=50)

    # Геоданные (на потом, пока заглушка)
    geo_polygon = models.JSONField('Полигон (GeoJSON)', null=True, blank=True)

    # Типы данных
    DATA_EXPERT = 'expert'
    DATA_MONITORING = 'monitoring'
    DATA_MIXED = 'mixed'
    DATA_CHOICES = [
        (DATA_EXPERT, 'Экспертный'),
        (DATA_MONITORING, 'Мониторинговый'),
        (DATA_MIXED, 'Смешанный'),
    ]
    data_type = models.CharField('Тип данных', max_length=20, choices=DATA_CHOICES, default=DATA_MIXED)

    # Дополнительные параметры
    settings = models.JSONField('Дополнительные настройки', default=dict, blank=True)

    # Метаданные
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
        ordering = ['region', 'name']
        unique_together = ['region', 'code']

    def __str__(self):
        return f"{self.region.name} - {self.name}"


class District(models.Model):
    """Район - третий уровень географической иерархии"""
    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        verbose_name='Город',
        related_name='districts'
    )
    name = models.CharField('Название', max_length=255)
    code = models.CharField('Код', max_length=50)

    # Геоданные (на потом, пока заглушка)
    geo_polygon = models.JSONField('Полигон (GeoJSON)', null=True, blank=True)

    # Типы данных
    DATA_EXPERT = 'expert'
    DATA_MONITORING = 'monitoring'
    DATA_MIXED = 'mixed'
    DATA_CHOICES = [
        (DATA_EXPERT, 'Экспертный'),
        (DATA_MONITORING, 'Мониторинговый'),
        (DATA_MIXED, 'Смешанный'),
    ]
    data_type = models.CharField('Тип данных', max_length=20, choices=DATA_CHOICES, default=DATA_MIXED)

    # Дополнительные параметры
    settings = models.JSONField('Дополнительные настройки', default=dict, blank=True)

    # Метаданные
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Район'
        verbose_name_plural = 'Районы'
        ordering = ['city', 'name']
        unique_together = ['city', 'code']

    def __str__(self):
        return f"{self.city.name} - {self.name}"


class Channel(models.Model):
    """Канал сбыта"""
    district = models.ForeignKey(
        District,
        on_delete=models.CASCADE,
        verbose_name='Район',
        related_name='channels',
        null=True,
        blank=True
    )
    name = models.CharField('Название', max_length=255)
    code = models.CharField('Код', max_length=50)

    # Тип канала
    TYPE_RETAIL = 'retail'
    TYPE_WHOLESALE = 'wholesale'
    TYPE_ONLINE = 'online'
    TYPE_HORECA = 'horeca'
    TYPE_OTHER = 'other'

    TYPE_CHOICES = [
        (TYPE_RETAIL, 'Розница'),
        (TYPE_WHOLESALE, 'Опт'),
        (TYPE_ONLINE, 'Онлайн'),
        (TYPE_HORECA, 'HoReCa'),
        (TYPE_OTHER, 'Другое'),
    ]
    type = models.CharField('Тип канала', max_length=50, choices=TYPE_CHOICES, default=TYPE_RETAIL)
    description = models.TextField('Описание', blank=True)

    # Дополнительные параметры
    settings = models.JSONField('Дополнительные настройки', default=dict, blank=True)

    # Метаданные
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Канал сбыта'
        verbose_name_plural = 'Каналы сбыта'
        ordering = ['district', 'name']
        unique_together = ['district', 'code']

    def __str__(self):
        return f"{self.district.name} - {self.name}"


class Outlet(models.Model):
    """Точка сбыта (магазин, торговая точка)"""
    channel = models.ForeignKey(
        Channel,
        on_delete=models.CASCADE,
        verbose_name='Канал',
        related_name='outlets'
    )
    name = models.CharField('Название', max_length=255)
    code = models.CharField('Код', max_length=50, blank=True)

    # Контактные данные
    address = models.TextField('Адрес', blank=True)
    contact_phone = models.CharField('Телефон', max_length=50, blank=True)
    contact_person = models.CharField('Контактное лицо', max_length=255, blank=True)

    # GPS координаты (на потом, пока просто поля)
    latitude = models.DecimalField('Широта', max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField('Долгота', max_digits=9, decimal_places=6, null=True, blank=True)

    # Фото
    photo = models.ImageField('Фото', upload_to='outlets/', blank=True, null=True)

    # Статус
    STATUS_ACTIVE = 'active'
    STATUS_INACTIVE = 'inactive'
    STATUS_CLOSED = 'closed'
    STATUS_CHOICES = [
        (STATUS_ACTIVE, 'Активна'),
        (STATUS_INACTIVE, 'Неактивна'),
        (STATUS_CLOSED, 'Закрыта'),
    ]
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default=STATUS_ACTIVE)

    # Дополнительные параметры
    settings = models.JSONField('Дополнительные настройки', default=dict, blank=True)

    # Метаданные
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Точка сбыта'
        verbose_name_plural = 'Точки сбыта'
        ordering = ['channel', 'name']

    def __str__(self):
        return f"{self.channel.name} - {self.name}"


class FootfallCounter(models.Model):
    """Счётчик проходимости торговой точки"""
    outlet = models.ForeignKey(
        Outlet,
        on_delete=models.CASCADE,
        verbose_name='Торговая точка',
        related_name='footfall_counts'
    )
    timestamp = models.DateTimeField(verbose_name="Время замера")
    count = models.IntegerField(verbose_name="Количество людей", help_text="За час")
    counted_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Подсчитано"
    )

    class Meta:
        verbose_name = "Проходимость"
        verbose_name_plural = "Проходимость"
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.outlet.name} - {self.count} чел/час ({self.timestamp.strftime('%d.%m.%Y %H:%M')})"


class OutletInventory(models.Model):
    """Наличие товаров в торговой точке"""
    outlet = models.ForeignKey(
        Outlet,
        on_delete=models.CASCADE,
        verbose_name='Торговая точка',
        related_name='inventory'
    )
    product = models.ForeignKey(
        'catalog.Product',
        on_delete=models.CASCADE,
        verbose_name='Товар'
    )
    quantity = models.IntegerField(verbose_name="Количество")
    last_updated = models.DateTimeField(auto_now=True, verbose_name="Обновлено")
    updated_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Обновил"
    )

    class Meta:
        verbose_name = "Наличие товара"
        verbose_name_plural = "Наличие товаров"
        unique_together = ['outlet', 'product']

    def __str__(self):
        return f"{self.product.name} в {self.outlet.name}: {self.quantity} шт"


class Display(models.Model):
    """Витрина/Прилавок в торговой точке"""
    DISPLAY_TYPES = [
        ('counter', 'Прилавок'),
        ('showcase', 'Витрина'),
        ('stand', 'Стенд'),
        ('wall', 'Стеллаж'),
    ]

    outlet = models.ForeignKey(
        Outlet,
        on_delete=models.CASCADE,
        verbose_name='Торговая точка',
        related_name='displays'
    )
    name = models.CharField(max_length=200, verbose_name="Название")
    display_type = models.CharField(max_length=50, choices=DISPLAY_TYPES, verbose_name="Тип")
    location = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Расположение",
        help_text="Например: У входа, Центр зала"
    )
    is_active = models.BooleanField(default=True, verbose_name="Активна")

    class Meta:
        verbose_name = "Витрина"
        verbose_name_plural = "Витрины"

    def __str__(self):
        return f"{self.get_display_type_display()} - {self.name} ({self.outlet.name})"


class DisplayInventory(models.Model):
    """Товары выложенные на витрине"""
    display = models.ForeignKey(
        Display,
        on_delete=models.CASCADE,
        verbose_name='Витрина',
        related_name='items'
    )
    product = models.ForeignKey(
        'catalog.Product',
        on_delete=models.CASCADE,
        verbose_name='Товар'
    )
    quantity = models.IntegerField(verbose_name="Количество")
    position = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Позиция",
        help_text="Например: Верхняя полка слева"
    )
    last_updated = models.DateTimeField(auto_now=True, verbose_name="Обновлено")

    class Meta:
        verbose_name = "Товар на витрине"
        verbose_name_plural = "Товары на витринах"
        unique_together = ['display', 'product']

    def __str__(self):
        return f"{self.product.name} на {self.display.name}: {self.quantity} шт"
