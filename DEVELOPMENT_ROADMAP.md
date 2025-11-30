# 🗺️ ПЛАН РАЗВИТИЯ СИСТЕМЫ DATUM

**Дата создания:** 2025-11-22
**Проект:** Datum - Система сбора полевых данных для ювелирного ритейла

---

## 📊 ТЕКУЩЕЕ СОСТОЯНИЕ СИСТЕМЫ

### Общая оценка по типам пользователей

| Пользователь | Текущая оценка | Основные проблемы |
|-------------|---------------|-------------------|
| **Полевые работники** (Mobile) | **5/10** | ❌ Нет оффлайн-режима<br>❌ Нет автосохранения<br>❌ Нет геолокации |
| **Аналитики** (Multi-device) | **3/10** | ❌ Дашборды показывают только JSON<br>❌ Нет графиков и визуализации<br>❌ Нет фильтров |
| **Просмотр отчетов** (Multi-device) | **2/10** | ❌ Отчеты — это RAW JSON<br>❌ Нет PDF генерации<br>❌ Нельзя использовать |

### Готовность функционала для сбора данных

- ✅ **57% метрик** можно собирать СЕЙЧАС (12 из 21)
- ⚠️ **19% метрик** требуют создания атрибутов (4 из 21)
- ❌ **24% метрик** требуют новых моделей (5 из 21)

### Критические отсутствующие функции

1. 🔴 **Визуализация дашбордов и отчетов** - система НЕ работает для аналитики
2. 🔴 **Progressive Web App (PWA)** - невозможна работа в оффлайн
3. 🔴 **Автосохранение форм** - риск потери данных
4. 🟡 **Фильтры для аналитики** - нельзя анализировать данные по периодам/регионам
5. 🟡 **PDF генерация** - нельзя распечатать отчеты
6. 🟡 **Геолокация** - нет проверки нахождения на точке
7. 🟡 **Множественная загрузка фото** - неудобный процесс фотофиксации

---

## 🎯 ПЛАН РАЗВИТИЯ

### **ФАЗА 1: МИНИМАЛЬНО ЖИЗНЕСПОСОБНЫЙ ПРОДУКТ** (2-3 недели)

**Цель:** Сделать систему РАБОТАЮЩЕЙ для всех типов пользователей

#### 1.1. Визуализация дашбордов с Chart.js 🔴 КРИТИЧНО

**Файлы для создания/модификации:**
- `analytics/views.py` - добавить `DashboardDetailView.get_context_data()`
- `analytics/views.py` - добавить методы `calculate_metric()`, `calculate_chart()`
- `templates/analytics/dashboard_detail.html` - заменить JSON на виджеты
- `templates/analytics/includes/metric_widget.html` - новый компонент
- `templates/analytics/includes/chart_widget.html` - новый компонент

**Реализация:**

```python
# analytics/views.py
from django.db.models import Avg, Count, Sum, Min, Max
from visits.models import Visit, Observation
from coefficients.models import Coefficient

class DashboardDetailView(LoginRequiredMixin, DetailView):
    model = Dashboard
    template_name = 'analytics/dashboard_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Парсить config JSON и вычислять метрики
        config = self.object.config or {}
        widgets = []

        for widget_config in config.get('widgets', []):
            if widget_config['type'] == 'metric':
                metric_data = self.calculate_metric(widget_config)
                widgets.append(metric_data)
            elif widget_config['type'] == 'chart':
                chart_data = self.calculate_chart(widget_config)
                widgets.append(chart_data)

        context['widgets'] = widgets
        return context

    def calculate_metric(self, config):
        """Вычислить числовую метрику"""
        coefficient_id = config.get('coefficient_id')
        aggregation = config.get('aggregation', 'avg')

        queryset = Observation.objects.filter(coefficient_id=coefficient_id)

        if aggregation == 'avg':
            value = queryset.aggregate(Avg('value_numeric'))['value_numeric__avg']
        elif aggregation == 'sum':
            value = queryset.aggregate(Sum('value_numeric'))['value_numeric__sum']
        elif aggregation == 'count':
            value = queryset.count()
        elif aggregation == 'min':
            value = queryset.aggregate(Min('value_numeric'))['value_numeric__min']
        elif aggregation == 'max':
            value = queryset.aggregate(Max('value_numeric'))['value_numeric__max']

        return {
            'type': 'metric',
            'title': config.get('title'),
            'value': round(value, 2) if value else 0,
            'unit': config.get('unit', ''),
            'color': config.get('color', 'primary'),
        }

    def calculate_chart(self, config):
        """Подготовить данные для графика"""
        coefficient_id = config.get('coefficient_id')
        chart_type = config.get('chart_type', 'line')
        group_by = config.get('group_by', 'date')

        # Группировка по датам
        if group_by == 'date':
            data = Observation.objects.filter(
                coefficient_id=coefficient_id
            ).extra(
                select={'date': "DATE(created_at)"}
            ).values('date').annotate(
                avg_value=Avg('value_numeric')
            ).order_by('date')

            labels = [item['date'].strftime('%d.%m.%Y') for item in data]
            values = [float(item['avg_value']) if item['avg_value'] else 0 for item in data]

        # Группировка по регионам
        elif group_by == 'region':
            data = Observation.objects.filter(
                coefficient_id=coefficient_id
            ).select_related(
                'visit__outlet__region'
            ).values(
                'visit__outlet__region__name'
            ).annotate(
                avg_value=Avg('value_numeric')
            ).order_by('-avg_value')

            labels = [item['visit__outlet__region__name'] for item in data]
            values = [float(item['avg_value']) if item['avg_value'] else 0 for item in data]

        return {
            'type': 'chart',
            'title': config.get('title'),
            'chart_type': chart_type,
            'labels': labels,
            'values': values,
            'color': config.get('color', 'rgb(75, 192, 192)'),
        }
```

```html
<!-- templates/analytics/dashboard_detail.html -->
{% extends 'base.html' %}

{% block title %}{{ object.name }} - Datum{% endblock %}

{% block content %}
<div class="row mb-4">
    <div class="col">
        <h1 class="h2">
            <i class="bi bi-graph-up"></i> {{ object.name }}
        </h1>
        <p class="text-muted">{{ object.description }}</p>
    </div>
    <div class="col-auto">
        <button class="btn btn-primary" onclick="refreshDashboard()">
            <i class="bi bi-arrow-clockwise"></i> Обновить
        </button>
        <a href="{% url 'analytics:dashboard_update' object.pk %}" class="btn btn-warning">
            <i class="bi bi-pencil"></i> Настроить
        </a>
    </div>
</div>

<div class="row">
    {% for widget in widgets %}
    <div class="col-md-6 col-lg-{% if widget.type == 'metric' %}3{% else %}6{% endif %} mb-4">
        {% if widget.type == 'metric' %}
        <!-- Метрика -->
        <div class="card border-{{ widget.color }}">
            <div class="card-body text-center">
                <h6 class="text-muted text-uppercase small">{{ widget.title }}</h6>
                <h2 class="display-4 mb-0 text-{{ widget.color }}">
                    {{ widget.value }}
                    {% if widget.unit %}
                    <small class="text-muted fs-5">{{ widget.unit }}</small>
                    {% endif %}
                </h2>
            </div>
        </div>

        {% elif widget.type == 'chart' %}
        <!-- График -->
        <div class="card">
            <div class="card-header">
                <h5 class="mb-0">{{ widget.title }}</h5>
            </div>
            <div class="card-body">
                <canvas id="chart_{{ forloop.counter }}" height="200"></canvas>
            </div>
        </div>
        <script>
        new Chart(document.getElementById('chart_{{ forloop.counter }}'), {
            type: '{{ widget.chart_type }}',
            data: {
                labels: {{ widget.labels|safe }},
                datasets: [{
                    label: '{{ widget.title }}',
                    data: {{ widget.values|safe }},
                    backgroundColor: '{{ widget.color }}',
                    borderColor: '{{ widget.color }}',
                    borderWidth: 2,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
        </script>
        {% endif %}
    </div>
    {% empty %}
    <div class="col-12">
        <div class="alert alert-info">
            <i class="bi bi-info-circle"></i>
            Дашборд не настроен. <a href="{% url 'analytics:dashboard_update' object.pk %}">Настроить виджеты</a>
        </div>
    </div>
    {% endfor %}
</div>

<script>
function refreshDashboard() {
    location.reload();
}
</script>
{% endblock %}
```

**Пример конфигурации дашборда (JSON):**

```json
{
  "widgets": [
    {
      "type": "metric",
      "title": "Средняя цена",
      "coefficient_id": 1,
      "aggregation": "avg",
      "unit": "₽",
      "color": "primary"
    },
    {
      "type": "metric",
      "title": "Всего визитов",
      "coefficient_id": null,
      "aggregation": "count",
      "color": "success"
    },
    {
      "type": "chart",
      "title": "Динамика цен",
      "coefficient_id": 1,
      "chart_type": "line",
      "group_by": "date",
      "color": "rgb(75, 192, 192)"
    },
    {
      "type": "chart",
      "title": "Цены по регионам",
      "coefficient_id": 1,
      "chart_type": "bar",
      "group_by": "region",
      "color": "rgb(255, 99, 132)"
    }
  ]
}
```

**Результат:** ✅ Дашборды показывают живые данные с графиками

---

#### 1.2. Визуализация отчетов 🔴 КРИТИЧНО

**Файлы для создания/модификации:**
- `analytics/views.py` - модифицировать `ReportDetailView`
- `templates/analytics/report_detail.html` - заменить JSON на таблицы/графики

**Реализация:**

```python
# analytics/views.py
class ReportDetailView(LoginRequiredMixin, DetailView):
    model = Report
    template_name = 'analytics/report_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Парсить result JSON и подготовить для отображения
        result = self.object.result or {}

        # Преобразовать в структурированные данные
        tables = []
        charts = []

        for section_key, section_data in result.items():
            if isinstance(section_data, list):
                # Это таблица
                tables.append({
                    'title': section_key.replace('_', ' ').title(),
                    'data': section_data
                })
            elif isinstance(section_data, dict) and 'labels' in section_data:
                # Это график
                charts.append({
                    'title': section_key.replace('_', ' ').title(),
                    'type': section_data.get('type', 'bar'),
                    'labels': section_data.get('labels', []),
                    'values': section_data.get('values', [])
                })

        context['tables'] = tables
        context['charts'] = charts
        return context
```

```html
<!-- templates/analytics/report_detail.html -->
{% extends 'base.html' %}

{% block title %}{{ object.name }} - Datum{% endblock %}

{% block content %}
<div class="row mb-4">
    <div class="col">
        <h1 class="h2">
            <i class="bi bi-file-earmark-bar-graph"></i> {{ object.name }}
        </h1>
        <p class="text-muted">{{ object.description }}</p>
    </div>
    <div class="col-auto">
        <a href="{% url 'analytics:report_pdf' object.pk %}" class="btn btn-danger">
            <i class="bi bi-file-pdf"></i> Скачать PDF
        </a>
        <button class="btn btn-primary" onclick="window.print()">
            <i class="bi bi-printer"></i> Печать
        </button>
    </div>
</div>

<!-- Информация об отчете -->
<div class="row mb-4">
    <div class="col-md-6">
        <div class="card">
            <div class="card-body">
                <dl class="row mb-0">
                    <dt class="col-sm-4">Статус:</dt>
                    <dd class="col-sm-8">
                        {% if object.status == 'completed' %}
                            <span class="badge bg-success">Готов</span>
                        {% elif object.status == 'processing' %}
                            <span class="badge bg-warning">Обрабатывается</span>
                        {% else %}
                            <span class="badge bg-danger">Ошибка</span>
                        {% endif %}
                    </dd>

                    <dt class="col-sm-4">Создан:</dt>
                    <dd class="col-sm-8">{{ object.created_at|date:"d.m.Y H:i" }}</dd>

                    {% if object.template %}
                    <dt class="col-sm-4">Шаблон:</dt>
                    <dd class="col-sm-8">{{ object.template.name }}</dd>
                    {% endif %}
                </dl>
            </div>
        </div>
    </div>
</div>

<!-- Графики -->
{% if charts %}
<div class="row mb-4">
    {% for chart in charts %}
    <div class="col-md-6 mb-4">
        <div class="card">
            <div class="card-header">
                <h5 class="mb-0">{{ chart.title }}</h5>
            </div>
            <div class="card-body">
                <canvas id="chart_{{ forloop.counter }}" height="250"></canvas>
            </div>
        </div>
    </div>
    <script>
    new Chart(document.getElementById('chart_{{ forloop.counter }}'), {
        type: '{{ chart.type }}',
        data: {
            labels: {{ chart.labels|safe }},
            datasets: [{
                label: '{{ chart.title }}',
                data: {{ chart.values|safe }},
                backgroundColor: 'rgba(54, 162, 235, 0.5)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true
        }
    });
    </script>
    {% endfor %}
</div>
{% endif %}

<!-- Таблицы -->
{% if tables %}
{% for table in tables %}
<div class="card mb-4">
    <div class="card-header">
        <h5 class="mb-0">{{ table.title }}</h5>
    </div>
    <div class="card-body">
        <div class="table-responsive">
            <table class="table table-striped table-hover">
                <thead>
                    <tr>
                        {% for key in table.data.0.keys %}
                        <th>{{ key|title }}</th>
                        {% endfor %}
                    </tr>
                </thead>
                <tbody>
                    {% for row in table.data %}
                    <tr>
                        {% for value in row.values %}
                        <td>{{ value }}</td>
                        {% endfor %}
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</div>
{% endfor %}
{% endif %}

<!-- Сырые данные (для отладки) -->
<details class="mt-4">
    <summary class="btn btn-sm btn-outline-secondary">Показать сырые данные (JSON)</summary>
    <pre class="bg-light p-3 rounded mt-2"><code>{{ object.result|safe }}</code></pre>
</details>
{% endblock %}
```

**Результат:** ✅ Отчеты показывают таблицы и графики вместо JSON

---

#### 1.3. Progressive Web App (PWA) 🔴 КРИТИЧНО

**Файлы для создания:**
- `static/manifest.json` - манифест приложения
- `static/service-worker.js` - Service Worker для оффлайн
- `static/icons/icon-192.png` - иконка 192x192
- `static/icons/icon-512.png` - иконка 512x512
- Модифицировать `templates/base.html` - подключить PWA

**1. Создать манифест:**

```json
{
  "name": "Datum - Сбор полевых данных",
  "short_name": "Datum",
  "description": "Система сбора и анализа данных для ювелирного ритейла",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#0d6efd",
  "orientation": "portrait",
  "icons": [
    {
      "src": "/static/icons/icon-192.png",
      "sizes": "192x192",
      "type": "image/png",
      "purpose": "any maskable"
    },
    {
      "src": "/static/icons/icon-512.png",
      "sizes": "512x512",
      "type": "image/png",
      "purpose": "any maskable"
    }
  ]
}
```

**2. Создать Service Worker:**

```javascript
// static/service-worker.js
const CACHE_NAME = 'datum-v1.0.0';
const OFFLINE_URL = '/offline/';

const CACHE_URLS = [
    '/',
    '/offline/',
    '/static/css/bootstrap.min.css',
    '/static/js/bootstrap.bundle.min.js',
    'https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css',
    'https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css',
];

// Установка Service Worker
self.addEventListener('install', (event) => {
    console.log('[SW] Installing...');
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            console.log('[SW] Caching app shell');
            return cache.addAll(CACHE_URLS);
        })
    );
    self.skipWaiting();
});

// Активация Service Worker
self.addEventListener('activate', (event) => {
    console.log('[SW] Activating...');
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    if (cacheName !== CACHE_NAME) {
                        console.log('[SW] Deleting old cache:', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
    self.clients.claim();
});

// Обработка запросов
self.addEventListener('fetch', (event) => {
    // Только GET запросы
    if (event.request.method !== 'GET') {
        return;
    }

    event.respondWith(
        caches.match(event.request).then((cachedResponse) => {
            if (cachedResponse) {
                // Возвращаем из кэша
                return cachedResponse;
            }

            // Пытаемся загрузить из сети
            return fetch(event.request).then((response) => {
                // Не кэшируем не-200 ответы
                if (!response || response.status !== 200) {
                    return response;
                }

                // Кэшируем успешный ответ
                const responseToCache = response.clone();
                caches.open(CACHE_NAME).then((cache) => {
                    cache.put(event.request, responseToCache);
                });

                return response;
            }).catch(() => {
                // Если сеть недоступна, показываем оффлайн страницу
                return caches.match(OFFLINE_URL);
            });
        })
    );
});

// Background Sync для отправки данных когда появится сеть
self.addEventListener('sync', (event) => {
    if (event.tag === 'sync-visits') {
        event.waitUntil(syncVisits());
    }
});

async function syncVisits() {
    const db = await openIndexedDB();
    const pendingVisits = await db.getAll('pendingVisits');

    for (const visit of pendingVisits) {
        try {
            const response = await fetch('/visits/api/sync/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(visit)
            });

            if (response.ok) {
                await db.delete('pendingVisits', visit.id);
                console.log('[SW] Synced visit:', visit.id);
            }
        } catch (error) {
            console.error('[SW] Sync failed:', error);
        }
    }
}
```

**3. Модифицировать base.html:**

```html
<!-- templates/base.html -->
<head>
    <!-- ... existing head content ... -->

    <!-- PWA Manifest -->
    <link rel="manifest" href="/static/manifest.json">

    <!-- Theme color для mobile browsers -->
    <meta name="theme-color" content="#0d6efd">

    <!-- Apple Touch Icon -->
    <link rel="apple-touch-icon" href="/static/icons/icon-192.png">

    <!-- iOS meta tags -->
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="default">
    <meta name="apple-mobile-web-app-title" content="Datum">
</head>

<body>
    <!-- ... existing body content ... -->

    <!-- PWA Install Banner -->
    <div id="installBanner" class="alert alert-info alert-dismissible position-fixed bottom-0 start-0 end-0 m-3" style="display: none; z-index: 9999;">
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        <div class="d-flex align-items-center">
            <i class="bi bi-download fs-3 me-3"></i>
            <div>
                <strong>Установите приложение Datum</strong>
                <p class="mb-2 small">Работайте оффлайн и получайте быстрый доступ</p>
                <button id="installBtn" class="btn btn-primary btn-sm">
                    <i class="bi bi-plus-circle"></i> Установить
                </button>
            </div>
        </div>
    </div>

    <!-- Service Worker Registration -->
    <script>
        if ('serviceWorker' in navigator) {
            window.addEventListener('load', () => {
                navigator.serviceWorker.register('/static/service-worker.js')
                    .then((registration) => {
                        console.log('✅ Service Worker registered:', registration.scope);
                    })
                    .catch((error) => {
                        console.error('❌ Service Worker registration failed:', error);
                    });
            });
        }

        // PWA Install Prompt
        let deferredPrompt;

        window.addEventListener('beforeinstallprompt', (e) => {
            e.preventDefault();
            deferredPrompt = e;

            // Показать баннер установки
            document.getElementById('installBanner').style.display = 'block';
        });

        document.getElementById('installBtn')?.addEventListener('click', async () => {
            if (deferredPrompt) {
                deferredPrompt.prompt();
                const { outcome } = await deferredPrompt.userChoice;

                if (outcome === 'accepted') {
                    console.log('✅ PWA installed');
                }

                deferredPrompt = null;
                document.getElementById('installBanner').style.display = 'none';
            }
        });

        window.addEventListener('appinstalled', () => {
            console.log('✅ PWA was installed');
            document.getElementById('installBanner').style.display = 'none';
        });
    </script>
</body>
```

**4. Создать оффлайн страницу:**

```html
<!-- templates/offline.html -->
{% extends 'base.html' %}

{% block title %}Нет подключения - Datum{% endblock %}

{% block content %}
<div class="container text-center py-5">
    <i class="bi bi-wifi-off" style="font-size: 5rem; color: #6c757d;"></i>
    <h1 class="mt-4">Нет подключения к интернету</h1>
    <p class="text-muted">Пожалуйста, проверьте подключение и попробуйте снова</p>

    <button onclick="location.reload()" class="btn btn-primary mt-3">
        <i class="bi bi-arrow-clockwise"></i> Обновить страницу
    </button>

    <div class="mt-5">
        <h5>Вы можете:</h5>
        <ul class="list-unstyled">
            <li>✅ Просматривать закэшированные страницы</li>
            <li>✅ Заполнять визиты оффлайн (будут отправлены при подключении)</li>
            <li>❌ Загружать новые данные</li>
        </ul>
    </div>
</div>
{% endblock %}
```

**5. Настроить URL для оффлайн страницы:**

```python
# datum/urls.py
from django.views.generic import TemplateView

urlpatterns = [
    # ... existing patterns ...
    path('offline/', TemplateView.as_view(template_name='offline.html'), name='offline'),
]
```

**Результат:** ✅ Приложение работает оффлайн, можно установить на домашний экран

---

#### 1.4. Автосохранение форм 🔴 КРИТИЧНО

**Файлы для модификации:**
- `templates/visits/fill_visit.html` - добавить автосохранение
- `static/js/autosave.js` - новый файл с логикой автосохранения

**Создать файл автосохранения:**

```javascript
// static/js/autosave.js
class FormAutosave {
    constructor(formSelector, options = {}) {
        this.form = document.querySelector(formSelector);
        if (!this.form) {
            console.error('Form not found:', formSelector);
            return;
        }

        this.storageKey = options.storageKey || `autosave_${this.form.id || 'form'}`;
        this.interval = options.interval || 30000; // 30 секунд
        this.excludeFields = options.excludeFields || ['csrfmiddlewaretoken'];
        this.intervalId = null;

        this.init();
    }

    init() {
        // Восстановить данные при загрузке
        this.restore();

        // Запустить автосохранение
        this.startAutosave();

        // Очистить при успешной отправке
        this.form.addEventListener('submit', () => {
            this.clear();
        });

        console.log(`✅ Autosave initialized for ${this.storageKey}`);
    }

    startAutosave() {
        this.intervalId = setInterval(() => {
            this.save();
        }, this.interval);
    }

    save() {
        const formData = new FormData(this.form);
        const data = {};

        for (let [key, value] of formData.entries()) {
            if (!this.excludeFields.includes(key)) {
                data[key] = value;
            }
        }

        const autosaveData = {
            data: data,
            timestamp: Date.now(),
            url: window.location.pathname
        };

        try {
            localStorage.setItem(this.storageKey, JSON.stringify(autosaveData));
            this.showNotification('💾 Форма автоматически сохранена', 'success');
            console.log('✅ Form autosaved');
        } catch (error) {
            console.error('❌ Autosave failed:', error);
        }
    }

    restore() {
        try {
            const saved = localStorage.getItem(this.storageKey);
            if (!saved) return;

            const { data, timestamp, url } = JSON.parse(saved);

            // Проверить, что это та же страница
            if (url !== window.location.pathname) {
                return;
            }

            // Проверить возраст данных (не больше 24 часов)
            const ageHours = (Date.now() - timestamp) / (1000 * 60 * 60);
            if (ageHours > 24) {
                this.clear();
                return;
            }

            const ageMinutes = Math.round((Date.now() - timestamp) / (1000 * 60));

            // Спросить пользователя
            if (confirm(`Найдено несохраненное заполнение формы (${ageMinutes} мин назад).\n\nВосстановить данные?`)) {
                this.fillForm(data);
                this.showNotification('✅ Данные восстановлены из автосохранения', 'info');
            } else {
                this.clear();
            }
        } catch (error) {
            console.error('❌ Restore failed:', error);
        }
    }

    fillForm(data) {
        Object.keys(data).forEach(key => {
            const input = this.form.querySelector(`[name="${key}"]`);
            if (!input) return;

            if (input.type === 'checkbox') {
                input.checked = data[key] === 'on' || data[key] === true;
            } else if (input.type === 'radio') {
                const radio = this.form.querySelector(`[name="${key}"][value="${data[key]}"]`);
                if (radio) radio.checked = true;
            } else {
                input.value = data[key];
            }
        });
    }

    clear() {
        localStorage.removeItem(this.storageKey);
        console.log('🗑️ Autosave cleared');
    }

    showNotification(message, type = 'info') {
        // Создать toast уведомление
        const toast = document.createElement('div');
        toast.className = `alert alert-${type} alert-dismissible position-fixed top-0 end-0 m-3`;
        toast.style.zIndex = '9999';
        toast.innerHTML = `
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            <small>${message}</small>
        `;
        document.body.appendChild(toast);

        setTimeout(() => {
            toast.remove();
        }, 3000);
    }

    destroy() {
        if (this.intervalId) {
            clearInterval(this.intervalId);
        }
    }
}

// Экспорт для использования
window.FormAutosave = FormAutosave;
```

**Модифицировать fill_visit.html:**

```html
<!-- templates/visits/fill_visit.html -->
{% extends 'base.html' %}

{% block extra_js %}
<script src="/static/js/autosave.js"></script>
<script>
document.addEventListener('DOMContentLoaded', function() {
    // Инициализировать автосохранение
    const autosave = new FormAutosave('form', {
        storageKey: 'visit_{{ visit.id }}_autosave',
        interval: 30000, // 30 секунд
        excludeFields: ['csrfmiddlewaretoken']
    });

    // Показать индикатор автосохранения
    const autosaveIndicator = document.createElement('div');
    autosaveIndicator.className = 'text-muted small mt-2';
    autosaveIndicator.innerHTML = '<i class="bi bi-cloud-check"></i> Автосохранение активно (каждые 30 сек)';
    document.querySelector('form').insertBefore(
        autosaveIndicator,
        document.querySelector('form').firstChild
    );
});
</script>
{% endblock %}
```

**Результат:** ✅ Формы автоматически сохраняются каждые 30 сек, данные восстанавливаются при перезагрузке

---

### **ФАЗА 2: ПОЛНОФУНКЦИОНАЛЬНАЯ СИСТЕМА** (1-2 недели)

**Цель:** Сделать систему УДОБНОЙ и ФУНКЦИОНАЛЬНОЙ

#### 2.1. Фильтры для аналитики 🟡

**Создать компонент фильтров:**

```html
<!-- templates/analytics/includes/filters.html -->
<div class="card mb-4">
    <div class="card-header">
        <div class="d-flex justify-content-between align-items-center">
            <h5 class="mb-0"><i class="bi bi-funnel"></i> Фильтры</h5>
            <button type="button" class="btn btn-sm btn-outline-secondary" onclick="resetFilters()">
                <i class="bi bi-arrow-clockwise"></i> Сбросить
            </button>
        </div>
    </div>
    <div class="card-body">
        <form method="get" id="filterForm">
            <div class="row g-3">
                <!-- Период -->
                <div class="col-md-3">
                    <label class="form-label">Период</label>
                    <select name="period" class="form-select" onchange="toggleCustomDates()">
                        <option value="today">Сегодня</option>
                        <option value="yesterday">Вчера</option>
                        <option value="week">Эта неделя</option>
                        <option value="last_week">Прошлая неделя</option>
                        <option value="month">Этот месяц</option>
                        <option value="last_month">Прошлый месяц</option>
                        <option value="quarter">Квартал</option>
                        <option value="year">Год</option>
                        <option value="custom">Свой период</option>
                    </select>
                </div>

                <!-- Даты (для custom) -->
                <div class="col-md-3" id="customDates" style="display: none;">
                    <label class="form-label">От - До</label>
                    <div class="input-group">
                        <input type="date" name="date_from" class="form-control">
                        <input type="date" name="date_to" class="form-control">
                    </div>
                </div>

                <!-- Регион -->
                <div class="col-md-2">
                    <label class="form-label">Регион</label>
                    <select name="region" class="form-select">
                        <option value="">Все</option>
                        {% for region in regions %}
                        <option value="{{ region.id }}">{{ region.name }}</option>
                        {% endfor %}
                    </select>
                </div>

                <!-- Канал -->
                <div class="col-md-2">
                    <label class="form-label">Канал</label>
                    <select name="channel" class="form-select">
                        <option value="">Все</option>
                        {% for channel in channels %}
                        <option value="{{ channel.id }}">{{ channel.name }}</option>
                        {% endfor %}
                    </select>
                </div>

                <!-- Категория товара -->
                <div class="col-md-2">
                    <label class="form-label">Категория</label>
                    <select name="category" class="form-select">
                        <option value="">Все</option>
                        {% for category in categories %}
                        <option value="{{ category.id }}">{{ category.name }}</option>
                        {% endfor %}
                    </select>
                </div>

                <!-- Кнопки -->
                <div class="col-md-12">
                    <button type="submit" class="btn btn-primary">
                        <i class="bi bi-search"></i> Применить фильтры
                    </button>
                    <button type="button" class="btn btn-outline-secondary" onclick="saveFilterPreset()">
                        <i class="bi bi-bookmark"></i> Сохранить фильтр
                    </button>
                </div>
            </div>
        </form>
    </div>
</div>

<script>
function toggleCustomDates() {
    const period = document.querySelector('[name="period"]').value;
    const customDates = document.getElementById('customDates');
    customDates.style.display = period === 'custom' ? 'block' : 'none';
}

function resetFilters() {
    window.location.href = window.location.pathname;
}

function saveFilterPreset() {
    const name = prompt('Название фильтра:');
    if (!name) return;

    const formData = new FormData(document.getElementById('filterForm'));
    const filters = Object.fromEntries(formData.entries());

    fetch('/analytics/filter-presets/create/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}'
        },
        body: JSON.stringify({
            name: name,
            filters: filters
        })
    }).then(response => {
        if (response.ok) {
            alert('✅ Фильтр сохранен!');
        }
    });
}
</script>
```

**Модифицировать views для применения фильтров:**

```python
# analytics/views.py
from datetime import datetime, timedelta
from django.utils import timezone

class DashboardDetailView(LoginRequiredMixin, DetailView):
    model = Dashboard

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Получить фильтры из GET параметров
        filters = self.get_filters()

        # Применить фильтры к данным
        # ... (передать filters в calculate_metric и calculate_chart)

        context['filters'] = filters
        context['regions'] = Region.objects.all()
        context['channels'] = Channel.objects.all()
        context['categories'] = Category.objects.all()
        return context

    def get_filters(self):
        period = self.request.GET.get('period', 'month')

        # Вычислить даты на основе периода
        now = timezone.now()

        if period == 'today':
            date_from = now.replace(hour=0, minute=0, second=0)
            date_to = now
        elif period == 'yesterday':
            date_from = (now - timedelta(days=1)).replace(hour=0, minute=0, second=0)
            date_to = now.replace(hour=0, minute=0, second=0)
        elif period == 'week':
            date_from = now - timedelta(days=now.weekday())
            date_to = now
        elif period == 'month':
            date_from = now.replace(day=1, hour=0, minute=0, second=0)
            date_to = now
        elif period == 'custom':
            date_from = self.request.GET.get('date_from')
            date_to = self.request.GET.get('date_to')

        return {
            'period': period,
            'date_from': date_from,
            'date_to': date_to,
            'region': self.request.GET.get('region'),
            'channel': self.request.GET.get('channel'),
            'category': self.request.GET.get('category'),
        }
```

**Результат:** ✅ Можно фильтровать данные по периодам, регионам, каналам

---

#### 2.2. PDF генерация отчетов 🟡

**Установить библиотеку:**

```bash
pip install weasyprint
```

**Создать view для PDF:**

```python
# analytics/views.py
from django.http import HttpResponse
from weasyprint import HTML
from django.template.loader import render_to_string

class ReportPDFView(LoginRequiredMixin, DetailView):
    model = Report

    def get(self, request, *args, **kwargs):
        report = self.get_object()

        # Подготовить данные
        context = {
            'report': report,
            'results': report.result or {},
            'generated_at': timezone.now(),
        }

        # Рендерить HTML шаблон
        html_string = render_to_string('analytics/report_pdf.html', context)

        # Конвертировать в PDF
        html = HTML(string=html_string, base_url=request.build_absolute_uri())
        pdf = html.write_pdf()

        # Вернуть PDF
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="report_{report.code}_{timezone.now().strftime("%Y%m%d")}.pdf"'
        return response
```

**Создать PDF шаблон:**

```html
<!-- templates/analytics/report_pdf.html -->
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{{ report.name }}</title>
    <style>
        @page {
            size: A4;
            margin: 2cm;
        }
        body {
            font-family: Arial, sans-serif;
            font-size: 12pt;
        }
        h1 {
            color: #0d6efd;
            border-bottom: 2px solid #0d6efd;
            padding-bottom: 10px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        th, td {
            border: 1px solid #dee2e6;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f8f9fa;
            font-weight: bold;
        }
        .header {
            text-align: right;
            color: #6c757d;
            font-size: 10pt;
            margin-bottom: 20px;
        }
        .footer {
            position: fixed;
            bottom: 0;
            width: 100%;
            text-align: center;
            font-size: 9pt;
            color: #6c757d;
        }
    </style>
</head>
<body>
    <div class="header">
        Дата создания: {{ generated_at|date:"d.m.Y H:i" }}
    </div>

    <h1>{{ report.name }}</h1>

    {% if report.description %}
    <p>{{ report.description }}</p>
    {% endif %}

    <div>
        <strong>Статус:</strong> {{ report.get_status_display }}<br>
        {% if report.template %}
        <strong>Шаблон:</strong> {{ report.template.name }}<br>
        {% endif %}
    </div>

    <hr>

    <!-- Таблицы с данными -->
    {% for section_key, section_data in results.items %}
    <h2>{{ section_key|title }}</h2>

    {% if section_data is list %}
    <table>
        <thead>
            <tr>
                {% for key in section_data.0.keys %}
                <th>{{ key|title }}</th>
                {% endfor %}
            </tr>
        </thead>
        <tbody>
            {% for row in section_data %}
            <tr>
                {% for value in row.values %}
                <td>{{ value }}</td>
                {% endfor %}
            </tr>
            {% endfor %}
        </tbody>
    </table>
    {% else %}
    <p>{{ section_data }}</p>
    {% endif %}
    {% endfor %}

    <div class="footer">
        Сгенерировано системой Datum &copy; 2025
    </div>
</body>
</html>
```

**Добавить URL:**

```python
# analytics/urls.py
path('reports/<int:pk>/pdf/', views.ReportPDFView.as_view(), name='report_pdf'),
```

**Результат:** ✅ Можно скачать отчеты в PDF

---

#### 2.3. Геолокация для визитов 🟡

**Модифицировать модель Visit:**

```python
# visits/models.py
class Visit(models.Model):
    # ... existing fields ...

    # Добавить поля геолокации
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        verbose_name="Широта"
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        verbose_name="Долгота"
    )
    location_verified = models.BooleanField(
        default=False,
        verbose_name="Локация подтверждена"
    )
    distance_from_outlet = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Расстояние от точки (м)"
    )
```

**Создать миграцию:**

```bash
python manage.py makemigrations
python manage.py migrate
```

**Добавить поля в Outlet (если их нет):**

```python
# geo/models.py
class Outlet(models.Model):
    # ... existing fields ...

    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )
```

**Модифицировать fill_visit.html:**

```html
<!-- templates/visits/fill_visit.html -->
{% block extra_js %}
<script>
// Геолокация
let userLocation = null;

function getLocation() {
    if ("geolocation" in navigator) {
        const locationBtn = document.getElementById('locationBtn');
        locationBtn.innerHTML = '<i class="bi bi-geo-alt"></i> Определение...';
        locationBtn.disabled = true;

        navigator.geolocation.getCurrentPosition(
            function(position) {
                userLocation = {
                    latitude: position.coords.latitude,
                    longitude: position.coords.longitude,
                    accuracy: position.coords.accuracy
                };

                // Установить значения в скрытые поля
                document.getElementById('latitude').value = userLocation.latitude;
                document.getElementById('longitude').value = userLocation.longitude;

                // Вычислить расстояние до точки
                const outletLat = {{ visit.outlet.latitude|default:0 }};
                const outletLon = {{ visit.outlet.longitude|default:0 }};

                if (outletLat && outletLon) {
                    const distance = calculateDistance(
                        userLocation.latitude,
                        userLocation.longitude,
                        outletLat,
                        outletLon
                    );

                    document.getElementById('distance').value = Math.round(distance);

                    // Показать статус
                    let statusHtml = '';
                    if (distance <= 50) {
                        statusHtml = `<div class="alert alert-success">
                            <i class="bi bi-check-circle-fill"></i>
                            Вы находитесь на точке (${Math.round(distance)}м)
                        </div>`;
                    } else if (distance <= 200) {
                        statusHtml = `<div class="alert alert-warning">
                            <i class="bi bi-exclamation-triangle-fill"></i>
                            Вы находитесь в ${Math.round(distance)}м от точки
                        </div>`;
                    } else {
                        statusHtml = `<div class="alert alert-danger">
                            <i class="bi bi-x-circle-fill"></i>
                            Вы находитесь далеко от точки (${Math.round(distance)}м)
                        </div>`;
                    }

                    document.getElementById('locationStatus').innerHTML = statusHtml;
                }

                locationBtn.innerHTML = '<i class="bi bi-geo-alt-fill"></i> Локация определена';
                locationBtn.classList.remove('btn-primary');
                locationBtn.classList.add('btn-success');
            },
            function(error) {
                console.error('Geolocation error:', error);
                locationBtn.innerHTML = '<i class="bi bi-geo-alt"></i> Ошибка определения';
                locationBtn.classList.add('btn-danger');

                alert('Не удалось определить местоположение. Пожалуйста, разрешите доступ к геолокации.');
            },
            {
                enableHighAccuracy: true,
                timeout: 10000,
                maximumAge: 0
            }
        );
    } else {
        alert('Геолокация не поддерживается вашим браузером');
    }
}

// Формула Haversine для вычисления расстояния
function calculateDistance(lat1, lon1, lat2, lon2) {
    const R = 6371e3; // Радиус Земли в метрах
    const φ1 = lat1 * Math.PI / 180;
    const φ2 = lat2 * Math.PI / 180;
    const Δφ = (lat2 - lat1) * Math.PI / 180;
    const Δλ = (lon2 - lon1) * Math.PI / 180;

    const a = Math.sin(Δφ/2) * Math.sin(Δφ/2) +
              Math.cos(φ1) * Math.cos(φ2) *
              Math.sin(Δλ/2) * Math.sin(Δλ/2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));

    return R * c; // расстояние в метрах
}

// Автоматически определить локацию при нажатии "Начать визит"
document.querySelector('[name="start_visit"]')?.addEventListener('click', function(e) {
    if (!userLocation) {
        e.preventDefault();
        getLocation();

        // Подождать 2 секунды и отправить форму
        setTimeout(() => {
            this.form.submit();
        }, 2000);
    }
});
</script>

<!-- Добавить в форму скрытые поля и кнопку -->
<input type="hidden" name="latitude" id="latitude">
<input type="hidden" name="longitude" id="longitude">
<input type="hidden" name="distance" id="distance">

<div class="card mb-3">
    <div class="card-header">
        <h5 class="mb-0"><i class="bi bi-geo-alt"></i> Геолокация</h5>
    </div>
    <div class="card-body">
        <button type="button" id="locationBtn" class="btn btn-primary" onclick="getLocation()">
            <i class="bi bi-geo-alt"></i> Определить местоположение
        </button>
        <div id="locationStatus" class="mt-3"></div>
        <small class="text-muted d-block mt-2">
            <i class="bi bi-info-circle"></i>
            Нажмите для определения вашего местоположения и проверки нахождения на точке
        </small>
    </div>
</div>
{% endblock %}
```

**Модифицировать view для сохранения геолокации:**

```python
# visits/views.py
class FillVisitView(LoginRequiredMixin, UpdateView):
    model = Visit
    # ... existing code ...

    def form_valid(self, form):
        # Сохранить геолокацию
        if self.request.POST.get('latitude'):
            form.instance.latitude = self.request.POST.get('latitude')
            form.instance.longitude = self.request.POST.get('longitude')
            form.instance.distance_from_outlet = self.request.POST.get('distance')

            # Проверить локацию (если в пределах 100м - подтвердить)
            distance = int(self.request.POST.get('distance', 999999))
            form.instance.location_verified = distance <= 100

        return super().form_valid(form)
```

**Результат:** ✅ Визиты автоматически фиксируют GPS координаты и проверяют нахождение на точке

---

#### 2.4. Множественная загрузка фото 🟡

**Модифицировать fill_visit.html для поддержки multiple:**

```html
<!-- templates/visits/fill_visit.html -->
{% elif field.field_type == 'image' %}
    <input
        type="file"
        name="{{ field.field_name }}"
        class="form-control form-control-lg"
        accept="image/*"
        capture="environment"
        multiple
        id="photos_{{ field.field_name }}"
        onchange="previewPhotos(this, 'preview_{{ field.field_name }}')"
        {% if field.required %}required{% endif %}>

    <small class="form-text text-muted">
        <i class="bi bi-camera"></i> Можно загрузить несколько фото
    </small>

    <!-- Превью фото -->
    <div id="preview_{{ field.field_name }}" class="row mt-3"></div>
{% endif %}

<script>
function previewPhotos(input, previewId) {
    const preview = document.getElementById(previewId);
    preview.innerHTML = '';

    if (!input.files || input.files.length === 0) {
        return;
    }

    Array.from(input.files).forEach((file, index) => {
        // Проверить размер файла (максимум 5MB)
        if (file.size > 5 * 1024 * 1024) {
            alert(`Файл ${file.name} слишком большой. Максимум 5MB`);
            return;
        }

        // Сжать изображение перед отправкой
        compressImage(file, (compressedBlob) => {
            const reader = new FileReader();
            reader.onload = function(e) {
                const col = document.createElement('div');
                col.className = 'col-6 col-md-4 col-lg-3 mb-3';
                col.innerHTML = `
                    <div class="card">
                        <img src="${e.target.result}" class="card-img-top" style="height: 150px; object-fit: cover;">
                        <div class="card-body p-2">
                            <small class="text-muted d-block text-truncate">${file.name}</small>
                            <small class="text-success">${formatFileSize(compressedBlob.size)}</small>
                            <button type="button" class="btn btn-sm btn-danger w-100 mt-1" onclick="removePhoto(this, ${index})">
                                <i class="bi bi-trash"></i> Удалить
                            </button>
                        </div>
                    </div>
                `;
                preview.appendChild(col);
            };
            reader.readAsDataURL(compressedBlob);
        });
    });
}

function compressImage(file, callback) {
    const reader = new FileReader();
    reader.onload = function(e) {
        const img = new Image();
        img.onload = function() {
            const canvas = document.createElement('canvas');
            let width = img.width;
            let height = img.height;

            // Максимальный размер 1920px
            const maxSize = 1920;
            if (width > height && width > maxSize) {
                height = (height * maxSize) / width;
                width = maxSize;
            } else if (height > maxSize) {
                width = (width * maxSize) / height;
                height = maxSize;
            }

            canvas.width = width;
            canvas.height = height;

            const ctx = canvas.getContext('2d');
            ctx.drawImage(img, 0, 0, width, height);

            canvas.toBlob(callback, 'image/jpeg', 0.8);
        };
        img.src = e.target.result;
    };
    reader.readAsDataURL(file);
}

function formatFileSize(bytes) {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
}

function removePhoto(btn, index) {
    btn.closest('.col-6').remove();
    // TODO: Удалить файл из input.files (требует пересоздания FileList)
}
</script>
```

**Модифицировать обработку на сервере:**

```python
# visits/views.py
from django.core.files.storage import default_storage

def handle_uploaded_photos(request, visit):
    """Обработка загруженных фото"""
    photos = request.FILES.getlist('photos')

    for photo in photos:
        # Создать запись VisitMedia
        VisitMedia.objects.create(
            visit=visit,
            media_type='photo',
            file=photo,
            caption=photo.name
        )
```

**Результат:** ✅ Можно загружать несколько фото за раз, с превью и сжатием

---

### **ФАЗА 3: ОПТИМИЗАЦИЯ И ДОПОЛНЕНИЯ** (1 неделя)

**Цель:** Сделать систему ОТЛИЧНОЙ

#### 3.1. Модели для недостающих метрик 🟢

**Создать новые модели:**

```python
# geo/models.py

class FootfallCounter(models.Model):
    """Счётчик проходимости торговой точки"""
    outlet = models.ForeignKey('Outlet', on_delete=models.CASCADE, related_name='footfall_counts')
    timestamp = models.DateTimeField(verbose_name="Время замера")
    count = models.IntegerField(verbose_name="Количество людей", help_text="За час")
    counted_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "Проходимость"
        verbose_name_plural = "Проходимость"
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.outlet.name} - {self.count} чел/час ({self.timestamp.strftime('%d.%m.%Y %H:%M')})"


class OutletInventory(models.Model):
    """Наличие товаров в торговой точке"""
    outlet = models.ForeignKey('Outlet', on_delete=models.CASCADE, related_name='inventory')
    product = models.ForeignKey('catalog.Product', on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name="Количество")
    last_updated = models.DateTimeField(auto_now=True, verbose_name="Обновлено")
    updated_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)

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

    outlet = models.ForeignKey('Outlet', on_delete=models.CASCADE, related_name='displays')
    name = models.CharField(max_length=200, verbose_name="Название")
    display_type = models.CharField(max_length=50, choices=DISPLAY_TYPES, verbose_name="Тип")
    location = models.CharField(max_length=200, blank=True, verbose_name="Расположение", help_text="Например: У входа, Центр зала")
    is_active = models.BooleanField(default=True, verbose_name="Активна")

    class Meta:
        verbose_name = "Витрина"
        verbose_name_plural = "Витрины"

    def __str__(self):
        return f"{self.get_display_type_display()} - {self.name} ({self.outlet.name})"


class DisplayInventory(models.Model):
    """Товары выложенные на витрине"""
    display = models.ForeignKey('Display', on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('catalog.Product', on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name="Количество")
    position = models.CharField(max_length=100, blank=True, verbose_name="Позиция", help_text="Например: Верхняя полка слева")
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Товар на витрине"
        verbose_name_plural = "Товары на витринах"
        unique_together = ['display', 'product']

    def __str__(self):
        return f"{self.product.name} на {self.display.name}: {self.quantity} шт"


# visits/models.py

class Sale(models.Model):
    """Продажа товара"""
    outlet = models.ForeignKey('geo.Outlet', on_delete=models.CASCADE, related_name='sales')
    product = models.ForeignKey('catalog.Product', on_delete=models.CASCADE, related_name='sales')
    quantity = models.IntegerField(verbose_name="Количество")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена за единицу")
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Сумма")
    sale_date = models.DateTimeField(verbose_name="Дата продажи")
    recorded_at = models.DateTimeField(auto_now_add=True, verbose_name="Зафиксировано")
    recorded_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "Продажа"
        verbose_name_plural = "Продажи"
        ordering = ['-sale_date']

    def save(self, *args, **kwargs):
        self.total_amount = self.quantity * self.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} - {self.quantity} шт x {self.price}₽ = {self.total_amount}₽"
```

**Создать миграции:**

```bash
python manage.py makemigrations geo visits
python manage.py migrate
```

**Зарегистрировать в admin:**

```python
# geo/admin.py
from .models import FootfallCounter, OutletInventory, Display, DisplayInventory

@admin.register(FootfallCounter)
class FootfallCounterAdmin(admin.ModelAdmin):
    list_display = ['outlet', 'timestamp', 'count', 'counted_by']
    list_filter = ['outlet__region', 'timestamp']
    search_fields = ['outlet__name']

@admin.register(OutletInventory)
class OutletInventoryAdmin(admin.ModelAdmin):
    list_display = ['outlet', 'product', 'quantity', 'last_updated']
    list_filter = ['outlet__region', 'outlet__channel']
    search_fields = ['outlet__name', 'product__name']

@admin.register(Display)
class DisplayAdmin(admin.ModelAdmin):
    list_display = ['name', 'display_type', 'outlet', 'location', 'is_active']
    list_filter = ['display_type', 'outlet__region']

@admin.register(DisplayInventory)
class DisplayInventoryAdmin(admin.ModelAdmin):
    list_display = ['display', 'product', 'quantity', 'position']
    list_filter = ['display__outlet__region']

# visits/admin.py
@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ['product', 'outlet', 'quantity', 'price', 'total_amount', 'sale_date']
    list_filter = ['sale_date', 'outlet__region']
    search_fields = ['product__name', 'outlet__name']
```

**Результат:** ✅ Все 21 метрика могут быть собраны и проанализированы

---

#### 3.2. Мобильная оптимизация интерфейсов 🟢

**Улучшения для fill_visit.html:**

```html
<!-- templates/visits/fill_visit.html -->

{% block extra_css %}
<style>
/* Мобильные улучшения */
@media (max-width: 768px) {
    /* Увеличить размер всех полей ввода */
    .form-control, .form-select {
        font-size: 16px !important; /* Предотвратить zoom на iOS */
        min-height: 48px;
    }

    /* Sticky футер с кнопками */
    .sticky-actions {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: white;
        border-top: 2px solid #dee2e6;
        padding: 10px;
        box-shadow: 0 -4px 6px rgba(0,0,0,0.1);
        z-index: 1000;
    }

    /* Отступ снизу для контента */
    .main-content {
        padding-bottom: 80px;
    }

    /* Прогресс-бар заполнения */
    .progress-bar-container {
        position: sticky;
        top: 56px;
        z-index: 999;
        background: white;
        padding: 10px;
        border-bottom: 1px solid #dee2e6;
    }
}

/* Аккордеоны для группировки полей */
.field-group {
    border: 1px solid #dee2e6;
    border-radius: 8px;
    margin-bottom: 15px;
}

.field-group-header {
    background: #f8f9fa;
    padding: 15px;
    cursor: pointer;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.field-group-body {
    padding: 15px;
    display: none;
}

.field-group-body.show {
    display: block;
}
</style>
{% endblock %}

<!-- Прогресс-бар -->
<div class="progress-bar-container d-md-none">
    <div class="d-flex justify-content-between mb-2">
        <small class="text-muted">Заполнено</small>
        <small class="text-muted"><span id="progressPercent">0</span>%</small>
    </div>
    <div class="progress">
        <div id="progressBar" class="progress-bar" role="progressbar" style="width: 0%"></div>
    </div>
</div>

<!-- Группировка полей в аккордеоны -->
<div class="field-group">
    <div class="field-group-header" onclick="toggleGroup(this)">
        <span><i class="bi bi-file-text"></i> Основная информация</span>
        <i class="bi bi-chevron-down"></i>
    </div>
    <div class="field-group-body show">
        <!-- Поля формы -->
    </div>
</div>

<!-- Sticky футер с кнопками (только на мобильных) -->
<div class="sticky-actions d-md-none">
    <div class="d-grid gap-2">
        {% if visit.status == 'in_progress' %}
            <button type="submit" class="btn btn-success btn-lg">
                <i class="bi bi-check-circle-fill"></i> Завершить визит
            </button>
        {% endif %}
    </div>
</div>

<script>
// Переключение аккордеонов
function toggleGroup(header) {
    const body = header.nextElementSibling;
    const icon = header.querySelector('.bi-chevron-down, .bi-chevron-up');

    body.classList.toggle('show');
    icon.classList.toggle('bi-chevron-down');
    icon.classList.toggle('bi-chevron-up');
}

// Прогресс заполнения
function updateProgress() {
    const inputs = document.querySelectorAll('input[required], select[required], textarea[required]');
    let filled = 0;

    inputs.forEach(input => {
        if (input.type === 'checkbox') {
            if (input.checked) filled++;
        } else if (input.value.trim() !== '') {
            filled++;
        }
    });

    const percent = Math.round((filled / inputs.length) * 100);
    document.getElementById('progressPercent').textContent = percent;
    document.getElementById('progressBar').style.width = percent + '%';
}

// Обновлять прогресс при изменении полей
document.querySelectorAll('input, select, textarea').forEach(element => {
    element.addEventListener('change', updateProgress);
    element.addEventListener('input', updateProgress);
});

// Начальный расчет
updateProgress();
</script>
```

**Результат:** ✅ Мобильный интерфейс оптимизирован с прогресс-баром, аккордеонами, sticky футером

---

#### 3.3. Real-time обновления дашбордов 🟢

**Добавить auto-refresh для дашбордов:**

```html
<!-- templates/analytics/dashboard_detail.html -->

<div class="row mb-4">
    <div class="col">
        <h1 class="h2">
            <i class="bi bi-graph-up"></i> {{ object.name }}
            <span id="lastUpdated" class="small text-muted"></span>
        </h1>
    </div>
    <div class="col-auto">
        <div class="btn-group">
            <button class="btn btn-outline-secondary" onclick="toggleAutoRefresh()">
                <i id="autoRefreshIcon" class="bi bi-pause-circle"></i>
                <span id="autoRefreshText">Авто-обновление</span>
            </button>
            <button class="btn btn-primary" onclick="refreshDashboard()">
                <i class="bi bi-arrow-clockwise"></i> Обновить
            </button>
        </div>
    </div>
</div>

<script>
let autoRefreshEnabled = false;
let autoRefreshInterval = null;
const REFRESH_INTERVAL = 60000; // 60 секунд

function refreshDashboard() {
    const loader = document.createElement('div');
    loader.className = 'position-fixed top-50 start-50 translate-middle';
    loader.innerHTML = '<div class="spinner-border text-primary" role="status"></div>';
    document.body.appendChild(loader);

    location.reload();
}

function toggleAutoRefresh() {
    autoRefreshEnabled = !autoRefreshEnabled;

    const icon = document.getElementById('autoRefreshIcon');
    const text = document.getElementById('autoRefreshText');

    if (autoRefreshEnabled) {
        icon.className = 'bi bi-play-circle-fill';
        text.textContent = 'Авто: ВКЛ';

        autoRefreshInterval = setInterval(refreshDashboard, REFRESH_INTERVAL);
        updateLastRefreshed();
    } else {
        icon.className = 'bi bi-pause-circle';
        text.textContent = 'Авто: ВЫКЛ';

        if (autoRefreshInterval) {
            clearInterval(autoRefreshInterval);
        }
    }
}

function updateLastRefreshed() {
    const now = new Date();
    document.getElementById('lastUpdated').textContent =
        `(обновлено ${now.toLocaleTimeString()})`;
}

// Показать время последнего обновления
updateLastRefreshed();
</script>
```

**Результат:** ✅ Дашборды могут автоматически обновляться каждую минуту

---

## ✅ ПОЛНЫЙ ЧЕКЛИСТ РЕАЛИЗАЦИИ

### 📱 Мобильная оптимизация для полевых работников

- [ ] **PWA установка**
  - [ ] Создать manifest.json
  - [ ] Создать Service Worker
  - [ ] Добавить иконки 192x192 и 512x512
  - [ ] Подключить в base.html
  - [ ] Создать offline.html страницу
  - [ ] Добавить Install Banner

- [ ] **Оффлайн работа**
  - [ ] Кэширование статических файлов
  - [ ] Кэширование страниц
  - [ ] IndexedDB для pending визитов
  - [ ] Background Sync API
  - [ ] Индикатор оффлайн режима

- [ ] **Автосохранение**
  - [ ] Создать autosave.js
  - [ ] Автосохранение каждые 30 сек в LocalStorage
  - [ ] Восстановление при перезагрузке
  - [ ] Очистка после успешной отправки
  - [ ] Уведомления об автосохранении

- [ ] **Геолокация**
  - [ ] Добавить поля latitude/longitude в Visit
  - [ ] Добавить distance_from_outlet
  - [ ] JavaScript для определения координат
  - [ ] Вычисление расстояния (Haversine)
  - [ ] Визуальная индикация статуса
  - [ ] Автоопределение при старте визита

- [ ] **UX улучшения**
  - [ ] Увеличенные поля (form-control-lg)
  - [ ] Увеличенные чекбоксы (3em)
  - [ ] Sticky футер с кнопками
  - [ ] Прогресс-бар заполнения
  - [ ] Аккордеоны для группировки
  - [ ] Font-size 16px (предотвращение zoom на iOS)

- [ ] **Фото**
  - [ ] Multiple загрузка
  - [ ] Превью фото
  - [ ] Сжатие перед отправкой
  - [ ] Удаление фото
  - [ ] Индикация размера

---

### 📊 Визуализация и аналитика

- [ ] **Дашборды**
  - [ ] Модифицировать DashboardDetailView
  - [ ] Метод calculate_metric()
  - [ ] Метод calculate_chart()
  - [ ] Шаблон с виджетами
  - [ ] Chart.js интеграция
  - [ ] Конфигурация через JSON
  - [ ] Примеры конфигураций

- [ ] **Отчеты**
  - [ ] Модифицировать ReportDetailView
  - [ ] Парсинг result JSON
  - [ ] Рендеринг таблиц
  - [ ] Рендеринг графиков
  - [ ] Кнопка "Печать"
  - [ ] Сырые данные в <details>

- [ ] **PDF генерация**
  - [ ] Установить WeasyPrint
  - [ ] Создать ReportPDFView
  - [ ] Шаблон report_pdf.html
  - [ ] CSS для печати
  - [ ] Добавить URL
  - [ ] Кнопка скачивания

- [ ] **Фильтры**
  - [ ] Компонент filters.html
  - [ ] Фильтр по периоду
  - [ ] Фильтр по региону
  - [ ] Фильтр по каналу
  - [ ] Фильтр по категории
  - [ ] Custom даты
  - [ ] Сохранение пресетов
  - [ ] Применение в views

- [ ] **Real-time**
  - [ ] Auto-refresh переключатель
  - [ ] Интервал обновления (60 сек)
  - [ ] Индикатор последнего обновления
  - [ ] Loader при обновлении

---

### 🗄️ Модели данных

- [ ] **FootfallCounter**
  - [ ] Создать модель
  - [ ] Миграция
  - [ ] Admin интерфейс
  - [ ] CRUD views
  - [ ] Шаблоны

- [ ] **OutletInventory**
  - [ ] Создать модель
  - [ ] Миграция
  - [ ] Admin интерфейс
  - [ ] CRUD views
  - [ ] Шаблоны

- [ ] **Display**
  - [ ] Создать модель
  - [ ] Миграция
  - [ ] Admin интерфейс
  - [ ] CRUD views
  - [ ] Шаблоны

- [ ] **DisplayInventory**
  - [ ] Создать модель
  - [ ] Миграция
  - [ ] Admin интерфейс
  - [ ] CRUD views
  - [ ] Шаблоны

- [ ] **Sale**
  - [ ] Создать модель
  - [ ] Миграция
  - [ ] Admin интерфейс
  - [ ] CRUD views
  - [ ] Шаблоны
  - [ ] Автовычисление total_amount

---

### 🎨 UI/UX компоненты

- [ ] **Адаптивные таблицы**
  - [ ] Horizontal scroll на мобильных
  - [ ] Responsive заголовки
  - [ ] Карточный вид для маленьких экранов

- [ ] **Виджеты метрик**
  - [ ] Большие числа
  - [ ] Цветовые индикаторы
  - [ ] % изменения
  - [ ] Sparkline графики

- [ ] **Навигация**
  - [ ] Breadcrumbs
  - [ ] Drill-down по данным
  - [ ] Back button

- [ ] **Уведомления**
  - [ ] Toast notifications
  - [ ] Success/Error/Warning
  - [ ] Auto-dismiss

---

### 🔧 Техническая инфраструктура

- [ ] **Зависимости**
  - [ ] WeasyPrint для PDF
  - [ ] Pillow для обработки изображений
  - [ ] python-dateutil для дат

- [ ] **Статические файлы**
  - [ ] service-worker.js
  - [ ] manifest.json
  - [ ] autosave.js
  - [ ] Иконки PWA

- [ ] **Настройки Django**
  - [ ] MEDIA_ROOT/MEDIA_URL
  - [ ] FILE_UPLOAD_MAX_MEMORY_SIZE
  - [ ] SECURE_SSL_REDIRECT для PWA

- [ ] **URL routing**
  - [ ] /offline/
  - [ ] /reports/<id>/pdf/
  - [ ] /dashboards/<id>/
  - [ ] /api/sync/ (для Background Sync)

---

### 📝 Документация

- [ ] **Руководства пользователя**
  - [ ] Как установить PWA
  - [ ] Как работать оффлайн
  - [ ] Как создать дашборд
  - [ ] Как настроить фильтры

- [ ] **Технические гайды**
  - [ ] Конфигурация дашбордов (JSON schema)
  - [ ] Формат result для отчетов
  - [ ] API для синхронизации

- [ ] **Примеры**
  - [ ] Примеры дашбордов
  - [ ] Примеры отчетов
  - [ ] Примеры фильтров

---

### 🧪 Тестирование

- [ ] **Функциональное**
  - [ ] Автосохранение работает
  - [ ] PWA устанавливается
  - [ ] Оффлайн режим работает
  - [ ] Геолокация определяется
  - [ ] Фото загружаются

- [ ] **Кроссбраузерное**
  - [ ] Chrome (Android)
  - [ ] Safari (iOS)
  - [ ] Firefox
  - [ ] Edge

- [ ] **Устройства**
  - [ ] iPhone (разные размеры)
  - [ ] Android (разные размеры)
  - [ ] Планшеты
  - [ ] Desktop

- [ ] **Производительность**
  - [ ] Lighthouse score > 90
  - [ ] Time to Interactive < 3s
  - [ ] First Contentful Paint < 1.5s

---

## 📈 МЕТРИКИ УСПЕХА

### До внедрения
- ⚠️ Дашборды: 0% функционал (показывают JSON)
- ⚠️ Отчеты: 0% функционал (показывают JSON)
- ⚠️ Мобильный UX: 50% (работает, но неудобно)
- ⚠️ Оффлайн: 0% (не работает)

### После Фазы 1 (MVP)
- ✅ Дашборды: 80% функционал
- ✅ Отчеты: 70% функционал
- ✅ Мобильный UX: 80%
- ✅ Оффлайн: 90%

### После Фазы 2 (Полный функционал)
- ✅ Дашборды: 95% функционал
- ✅ Отчеты: 95% функционал (с PDF)
- ✅ Мобильный UX: 90%
- ✅ Все 21 метрика собираются

### После Фазы 3 (Оптимизация)
- ✅ Дашборды: 100% функционал
- ✅ Отчеты: 100% функционал
- ✅ Мобильный UX: 95%
- ✅ Real-time обновления
- ✅ Полная оптимизация

---

## 🎯 ПРИОРИТИЗАЦИЯ

### 🔴 КРИТИЧНО (Делать ПЕРВЫМИ)
1. Визуализация дашбордов
2. Визуализация отчетов
3. PWA (Service Worker + Manifest)
4. Автосохранение форм

**Без этого система НЕ РАБОТАЕТ**

### 🟡 ВАЖНО (Второй приоритет)
5. Фильтры аналитики
6. PDF генерация
7. Геолокация
8. Множественные фото

**Это делает систему УДОБНОЙ**

### 🟢 ДОПОЛНИТЕЛЬНО (Третий приоритет)
9. Новые модели (FootfallCounter, etc)
10. Мобильная оптимизация (аккордеоны, прогресс-бар)
11. Real-time обновления

**Это делает систему ОТЛИЧНОЙ**

---

## 📅 TIMELINE

### Неделя 1-2: ФАЗА 1 - MVP
**Цель:** Сделать работающую систему

- День 1-3: Визуализация дашбордов
- День 4-5: Визуализация отчетов
- День 6-8: PWA реализация
- День 9-10: Автосохранение

**Результат:** ✅ Система полностью работоспособна

### Неделя 3: ФАЗА 2 - Функционал
**Цель:** Добавить важные функции

- День 11-12: Фильтры
- День 13-14: PDF генерация
- День 15-16: Геолокация
- День 17: Множественные фото

**Результат:** ✅ Система функциональна и удобна

### Неделя 4: ФАЗА 3 - Оптимизация
**Цель:** Довести до совершенства

- День 18-19: Новые модели
- День 20-21: Мобильная оптимизация
- День 22: Real-time обновления
- День 23-24: Тестирование и баг-фиксы

**Результат:** ✅ Система отличная и готова к production

---

## 🚀 DEPLOYMENT CHECKLIST

### Перед деплоем на production
- [ ] Все миграции применены
- [ ] Собраны static файлы (`collectstatic`)
- [ ] HTTPS настроен (обязательно для PWA)
- [ ] Service Worker работает на HTTPS
- [ ] Иконки PWA созданы
- [ ] PDF генерация работает (установлен WeasyPrint)
- [ ] Backup базы данных
- [ ] Мониторинг настроен
- [ ] Логи настроены
- [ ] Performance тесты пройдены

### После деплоя
- [ ] Протестировать PWA установку
- [ ] Протестировать оффлайн режим
- [ ] Протестировать автосохранение
- [ ] Протестировать геолокацию
- [ ] Протестировать PDF генерацию
- [ ] Протестировать на реальных устройствах
- [ ] Обучить пользователей

---

## 📞 ПОДДЕРЖКА И ОБРАТНАЯ СВЯЗЬ

### Контакты для вопросов
- **Техническая поддержка:** [создать канал]
- **Баги и предложения:** GitHub Issues
- **Документация:** [создать wiki]

### Сбор обратной связи
- Опросы пользователей после каждой фазы
- Мониторинг метрик использования
- A/B тестирование интерфейсов

---

**Дата последнего обновления:** 2025-11-22
**Версия плана:** 1.0
**Статус:** Готов к реализации ✅
