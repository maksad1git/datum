"""
Общие константы для всей системы DATUM
"""

# ============================================================================
# ТИПЫ ИСТОЧНИКОВ ДАННЫХ
# ============================================================================

DATA_SOURCE_MONITORING = 'MON'
DATA_SOURCE_EXPERT = 'EXP'
DATA_SOURCE_AI = 'AI'

DATA_SOURCE_CHOICES = [
    (DATA_SOURCE_MONITORING, 'Мониторинговые'),
    (DATA_SOURCE_EXPERT, 'Экспертные'),
    (DATA_SOURCE_AI, 'Данные ИИ'),
]

# Для формул - может быть CUSTOM (смешанные данные)
FORMULA_SOURCE_MONITORING = 'MON'
FORMULA_SOURCE_EXPERT = 'EXP'
FORMULA_SOURCE_AI = 'AI'
FORMULA_SOURCE_CUSTOM = 'CUSTOM'

FORMULA_SOURCE_CHOICES = [
    (FORMULA_SOURCE_MONITORING, 'Мониторинговые'),
    (FORMULA_SOURCE_EXPERT, 'Экспертные'),
    (FORMULA_SOURCE_AI, 'Данные ИИ'),
    (FORMULA_SOURCE_CUSTOM, 'Смешанные (Custom)'),
]

# ============================================================================
# ЦВЕТОВАЯ СХЕМА ДЛЯ UI
# ============================================================================

DATA_SOURCE_COLORS = {
    DATA_SOURCE_MONITORING: 'primary',  # Синий
    DATA_SOURCE_EXPERT: 'success',      # Зелёный
    DATA_SOURCE_AI: 'purple',           # Фиолетовый (потребует custom CSS)
}

DATA_SOURCE_ICONS = {
    DATA_SOURCE_MONITORING: 'bi-rulers',        # Измерительные инструменты
    DATA_SOURCE_EXPERT: 'bi-person-badge',      # Эксперт
    DATA_SOURCE_AI: 'bi-cpu',                   # Процессор/AI
}
