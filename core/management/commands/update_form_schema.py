from django.core.management.base import BaseCommand
from forms.models import FormTemplate
from coefficients.models import Coefficient


class Command(BaseCommand):
    help = 'Update FONON form template with comprehensive field schema'

    def handle(self, *args, **options):
        self.stdout.write("="*80)
        self.stdout.write("UPDATE FONON FORM TEMPLATE SCHEMA")
        self.stdout.write("="*80)

        # Get the FONON form template
        try:
            form_template = FormTemplate.objects.get(code='fonon_jewelry_monitoring')
            self.stdout.write(f"Found form template: {form_template.name}")
        except FormTemplate.DoesNotExist:
            self.stdout.write(self.style.ERROR("ERROR: FONON form template not found!"))
            return

        # Define comprehensive field schema
        fields_schema = [
            # SECTION 1: General Information
            {
                "id": "outlet_name",
                "type": "text",
                "label": "Название торговой точки",
                "placeholder": "Введите название магазина",
                "required": True,
                "order": 1,
                "section": "general"
            },
            {
                "id": "outlet_address",
                "type": "text",
                "label": "Адрес",
                "placeholder": "Полный адрес торговой точки",
                "required": True,
                "order": 2,
                "section": "general"
            },
            {
                "id": "visit_date",
                "type": "datetime",
                "label": "Дата и время визита",
                "required": True,
                "order": 3,
                "section": "general",
                "default": "now"
            },
            {
                "id": "channel_type",
                "type": "select",
                "label": "Тип канала",
                "options": ["Ювелирный магазин", "Бутик", "Универмаг", "Онлайн"],
                "required": True,
                "order": 4,
                "section": "general"
            },

            # SECTION 2: Foot Traffic & Store Count
            {
                "id": "passability",
                "type": "number",
                "label": "Проходимость (чел./час)",
                "unit": "чел./час",
                "coefficient_code": "passability",
                "required": True,
                "order": 10,
                "section": "traffic",
                "min": 0,
                "step": 1
            },
            {
                "id": "counter_count",
                "type": "number",
                "label": "Количество прилавков",
                "unit": "шт",
                "coefficient_code": "counter_count",
                "required": True,
                "order": 11,
                "section": "traffic",
                "min": 1,
                "step": 1
            },
            {
                "id": "total_items",
                "type": "number",
                "label": "Общее количество изделий в магазине",
                "unit": "шт",
                "coefficient_code": "total_items",
                "required": True,
                "order": 12,
                "section": "traffic",
                "min": 0,
                "step": 1
            },
            {
                "id": "items_per_counter",
                "type": "number",
                "label": "Количество изделий на прилавке",
                "unit": "шт",
                "coefficient_code": "items_per_counter",
                "required": False,
                "order": 13,
                "section": "traffic",
                "min": 0,
                "step": 1,
                "help_text": "Среднее количество изделий на один прилавок"
            },

            # SECTION 3: Premium Segment
            {
                "id": "premium_items",
                "type": "number",
                "label": "Количество изделий премиум сегмента",
                "unit": "шт",
                "coefficient_code": "premium_items",
                "required": True,
                "order": 20,
                "section": "premium",
                "min": 0,
                "step": 1
            },

            # SECTION 4: Metal Types
            {
                "id": "yellow_gold_items",
                "type": "number",
                "label": "Изделия из желтого золота",
                "unit": "шт",
                "coefficient_code": "yellow_gold_items",
                "required": True,
                "order": 30,
                "section": "metals",
                "min": 0,
                "step": 1
            },
            {
                "id": "red_gold_items",
                "type": "number",
                "label": "Изделия из красного золота",
                "unit": "шт",
                "coefficient_code": "red_gold_items",
                "required": True,
                "order": 31,
                "section": "metals",
                "min": 0,
                "step": 1
            },
            {
                "id": "white_gold_items",
                "type": "number",
                "label": "Изделия из белого золота",
                "unit": "шт",
                "coefficient_code": "white_gold_items",
                "required": True,
                "order": 32,
                "section": "metals",
                "min": 0,
                "step": 1
            },

            # SECTION 5: Product Categories - Counts
            {
                "id": "ring_count",
                "type": "number",
                "label": "Количество колец",
                "unit": "шт",
                "coefficient_code": "ring_count",
                "required": True,
                "order": 40,
                "section": "categories",
                "min": 0,
                "step": 1
            },
            {
                "id": "earring_count",
                "type": "number",
                "label": "Количество серег",
                "unit": "шт",
                "coefficient_code": "earring_count",
                "required": True,
                "order": 41,
                "section": "categories",
                "min": 0,
                "step": 1
            },
            {
                "id": "chain_count",
                "type": "number",
                "label": "Количество цепочек",
                "unit": "шт",
                "coefficient_code": "chain_count",
                "required": True,
                "order": 42,
                "section": "categories",
                "min": 0,
                "step": 1
            },
            {
                "id": "bracelet_count",
                "type": "number",
                "label": "Количество браслетов",
                "unit": "шт",
                "coefficient_code": "bracelet_count",
                "required": True,
                "order": 43,
                "section": "categories",
                "min": 0,
                "step": 1
            },
            {
                "id": "pendant_count",
                "type": "number",
                "label": "Количество кулонов",
                "unit": "шт",
                "coefficient_code": "pendant_count",
                "required": True,
                "order": 44,
                "section": "categories",
                "min": 0,
                "step": 1
            },
            {
                "id": "set_count",
                "type": "number",
                "label": "Количество комплектов",
                "unit": "шт",
                "coefficient_code": "set_count",
                "required": True,
                "order": 45,
                "section": "categories",
                "min": 0,
                "step": 1
            },

            # SECTION 6: Product Weights
            {
                "id": "ring_total_weight",
                "type": "number",
                "label": "Общий вес колец",
                "unit": "гр",
                "coefficient_code": "ring_total_weight",
                "required": False,
                "order": 50,
                "section": "weights",
                "min": 0,
                "step": 0.01,
                "help_text": "Суммарный вес всех колец для расчета среднего"
            },
            {
                "id": "earring_total_weight",
                "type": "number",
                "label": "Общий вес серег",
                "unit": "гр",
                "coefficient_code": "earring_total_weight",
                "required": False,
                "order": 51,
                "section": "weights",
                "min": 0,
                "step": 0.01
            },
            {
                "id": "chain_total_weight",
                "type": "number",
                "label": "Общий вес цепочек",
                "unit": "гр",
                "coefficient_code": "chain_total_weight",
                "required": False,
                "order": 52,
                "section": "weights",
                "min": 0,
                "step": 0.01
            },
            {
                "id": "bracelet_total_weight",
                "type": "number",
                "label": "Общий вес браслетов",
                "unit": "гр",
                "coefficient_code": "bracelet_total_weight",
                "required": False,
                "order": 53,
                "section": "weights",
                "min": 0,
                "step": 0.01
            },
            {
                "id": "pendant_total_weight",
                "type": "number",
                "label": "Общий вес кулонов",
                "unit": "гр",
                "coefficient_code": "pendant_total_weight",
                "required": False,
                "order": 54,
                "section": "weights",
                "min": 0,
                "step": 0.01
            },
            {
                "id": "set_total_weight",
                "type": "number",
                "label": "Общий вес комплектов",
                "unit": "гр",
                "coefficient_code": "set_total_weight",
                "required": False,
                "order": 55,
                "section": "weights",
                "min": 0,
                "step": 0.01
            },

            # SECTION 7: Sales Data
            {
                "id": "ring_sales",
                "type": "number",
                "label": "Продажи колец",
                "unit": "шт",
                "coefficient_code": "ring_sales",
                "required": False,
                "order": 60,
                "section": "sales",
                "min": 0,
                "step": 1,
                "help_text": "Количество проданных колец за период"
            },
            {
                "id": "earring_sales",
                "type": "number",
                "label": "Продажи серег",
                "unit": "шт",
                "coefficient_code": "earring_sales",
                "required": False,
                "order": 61,
                "section": "sales",
                "min": 0,
                "step": 1
            },
            {
                "id": "chain_sales",
                "type": "number",
                "label": "Продажи цепочек",
                "unit": "шт",
                "coefficient_code": "chain_sales",
                "required": False,
                "order": 62,
                "section": "sales",
                "min": 0,
                "step": 1
            },
            {
                "id": "bracelet_sales",
                "type": "number",
                "label": "Продажи браслетов",
                "unit": "шт",
                "coefficient_code": "bracelet_sales",
                "required": False,
                "order": 63,
                "section": "sales",
                "min": 0,
                "step": 1
            },
            {
                "id": "pendant_sales",
                "type": "number",
                "label": "Продажи кулонов",
                "unit": "шт",
                "coefficient_code": "pendant_sales",
                "required": False,
                "order": 64,
                "section": "sales",
                "min": 0,
                "step": 1
            },
            {
                "id": "set_sales",
                "type": "number",
                "label": "Продажи комплектов",
                "unit": "шт",
                "coefficient_code": "set_sales",
                "required": False,
                "order": 65,
                "section": "sales",
                "min": 0,
                "step": 1
            },

            # SECTION 8: Photos & Notes
            {
                "id": "storefront_photo",
                "type": "photo",
                "label": "Фото витрины магазина",
                "required": True,
                "order": 70,
                "section": "media",
                "max_files": 5
            },
            {
                "id": "counter_photos",
                "type": "photo",
                "label": "Фото прилавков",
                "required": False,
                "order": 71,
                "section": "media",
                "max_files": 10
            },
            {
                "id": "product_photos",
                "type": "photo",
                "label": "Фото изделий",
                "required": False,
                "order": 72,
                "section": "media",
                "max_files": 20
            },
            {
                "id": "notes",
                "type": "textarea",
                "label": "Примечания",
                "placeholder": "Дополнительные наблюдения, особенности магазина...",
                "required": False,
                "order": 80,
                "section": "notes",
                "rows": 5
            },
            {
                "id": "competitor_presence",
                "type": "checkbox",
                "label": "Наличие конкурентов",
                "required": False,
                "order": 81,
                "section": "notes"
            },
            {
                "id": "promo_materials",
                "type": "checkbox",
                "label": "Наличие промо материалов",
                "required": False,
                "order": 82,
                "section": "notes"
            }
        ]

        # Update form template with new schema
        form_template.fields_schema = fields_schema
        form_template.save()

        self.stdout.write(self.style.SUCCESS(f"\nSUCCESS! Updated form template with {len(fields_schema)} fields"))

        self.stdout.write("\nField sections:")
        sections = {}
        for field in fields_schema:
            section = field.get('section', 'unknown')
            sections[section] = sections.get(section, 0) + 1

        for section, count in sorted(sections.items()):
            self.stdout.write(f"  - {section}: {count} fields")

        self.stdout.write("\nFields linked to coefficients:")
        linked_count = sum(1 for field in fields_schema if 'coefficient_code' in field)
        self.stdout.write(f"  {linked_count} fields linked to coefficients")

        self.stdout.write("="*80)
