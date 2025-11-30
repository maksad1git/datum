"""
Модуль для загрузки предустановленных категорий и атрибутов из JSON файлов.
"""
import json
import os
from pathlib import Path
from django.conf import settings
from django.db import transaction
from .models import Category, AttributeGroup, AttributeDefinition


class PreinstallLoader:
    """Класс для загрузки предустановленных категорий"""

    PREINSTALL_DIR = Path(__file__).parent / 'preinstall'

    @classmethod
    def get_available_presets(cls):
        """Получить список доступных предустановок"""
        presets = []

        if not cls.PREINSTALL_DIR.exists():
            return presets

        for json_file in cls.PREINSTALL_DIR.glob('*.json'):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    meta = data.get('meta', {})

                    # Проверить, загружена ли уже эта категория
                    is_installed = cls.is_preset_installed(meta.get('code'))

                    presets.append({
                        'file': json_file.name,
                        'code': meta.get('code', ''),
                        'name': meta.get('name', json_file.stem),
                        'description': meta.get('description', ''),
                        'icon': meta.get('icon', 'box'),
                        'version': meta.get('version', '1.0'),
                        'is_installed': is_installed,
                    })
            except Exception as e:
                print(f"Error reading {json_file}: {e}")
                continue

        return sorted(presets, key=lambda x: x['name'])

    @classmethod
    def is_preset_installed(cls, code):
        """Проверить, установлена ли предустановка"""
        if not code:
            return False
        return Category.objects.filter(code=code).exists()

    @classmethod
    @transaction.atomic
    def load_preset(cls, filename):
        """Загрузить предустановку из JSON файла"""
        json_path = cls.PREINSTALL_DIR / filename

        if not json_path.exists():
            raise FileNotFoundError(f"Файл {filename} не найден")

        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Загрузить метаданные
        meta = data.get('meta', {})

        # Проверить, не установлено ли уже
        if cls.is_preset_installed(meta.get('code')):
            raise ValueError(f"Категория {meta.get('name')} уже установлена")

        # Словари для хранения созданных объектов
        categories_map = {}
        groups_map = {}

        # 1. Создать категории
        for cat_data in data.get('categories', []):
            parent = None
            if cat_data.get('parent'):
                parent = categories_map.get(cat_data['parent'])

            category = Category.objects.create(
                name=cat_data['name'],
                code=cat_data['code'],
                parent=parent
            )
            categories_map[cat_data['code']] = category

        # 2. Создать группы атрибутов
        for group_data in data.get('attribute_groups', []):
            category = categories_map.get(group_data['category'])

            group = AttributeGroup.objects.create(
                name=group_data['name'],
                code=group_data['code'],
                category=category,
                order=group_data.get('order', 0),
                is_active=True
            )
            groups_map[group_data['code']] = group

        # 3. Создать определения атрибутов
        for attr_data in data.get('attributes', []):
            group = groups_map.get(attr_data['group'])

            # Подготовить данные
            attr_params = {
                'name': attr_data['name'],
                'code': attr_data['code'],
                'group': group,
                'data_type': attr_data['data_type'],
                'is_required': attr_data.get('is_required', False),
                'is_filterable': attr_data.get('is_filterable', True),
                'is_searchable': attr_data.get('is_searchable', False),
                'order': attr_data.get('order', 0),
                'is_active': True,
            }

            # Дополнительные параметры
            if 'unit' in attr_data:
                attr_params['unit'] = attr_data['unit']
            if 'min_value' in attr_data:
                attr_params['min_value'] = attr_data['min_value']
            if 'max_value' in attr_data:
                attr_params['max_value'] = attr_data['max_value']
            if 'max_length' in attr_data:
                attr_params['max_length'] = attr_data['max_length']
            if 'choices' in attr_data:
                attr_params['choices'] = attr_data['choices']
            if 'placeholder' in attr_data:
                attr_params['placeholder'] = attr_data['placeholder']
            if 'help_text' in attr_data:
                attr_params['help_text'] = attr_data['help_text']

            AttributeDefinition.objects.create(**attr_params)

        return {
            'meta': meta,
            'categories_created': len(categories_map),
            'groups_created': len(groups_map),
            'attributes_created': len(data.get('attributes', [])),
        }
