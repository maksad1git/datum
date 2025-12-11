# DATUM - Mystery Shopping & Data Collection System

**Modern SPA Platform for Field Data Collection and Business Intelligence**

DATUM is a comprehensive mystery shopping and data collection platform designed for FMCG companies, retailers, and market research agencies. The system enables efficient data gathering, real-time analytics, and powerful insights across multi-level geographic hierarchies.

[![Django](https://img.shields.io/badge/Django-5.2.7-green.svg)](https://www.djangoproject.com/)
[![Vue.js](https://img.shields.io/badge/Vue.js-3.x-brightgreen.svg)](https://vuejs.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-3.x-blue.svg)](https://tailwindcss.com/)
[![Python](https://img.shields.io/badge/Python-3.13.9-blue.svg)](https://www.python.org/)

---

## 🚀 Key Features

### 📊 Data Collection & Mystery Shopping
- **Structured Visit Management** - VisitTypes, custom forms, photo/video uploads
- **Real-Time GPS Tracking** - Outlet check-ins with geolocation
- **Offline-First PWA** - Works without internet, syncs when online
- **EAV Attributes** - Flexible product attributes and observations

### 🗺️ Geographic Hierarchy (6 Levels)
- **Global Market** → **Country** → **Region** → **City** → **District** → **Channel** → **Outlet**
- Cascading dropdowns for easy navigation
- Multi-level dashboards with drill-down analytics

### 📈 Analytics & Business Intelligence
- **Multi-Level Dashboards** - Global, Country, Region, City, District views
- **Chart.js Visualizations** - Interactive charts and graphs
- **Custom Metrics** - Weighted KPIs with coefficient system
- **Export Capabilities** - Excel, CSV, PDF reports

### 🏪 Retail & FMCG Focus
- **Product Catalog** - Brands, Categories, Products with EAV attributes
- **Outlet Inventory** - Stock tracking and availability
- **Display Management** - POS materials and merchandising
- **Footfall Counters** - Outlet traffic monitoring

### 🔐 Enterprise Security
- **JWT Authentication** - Secure token-based auth
- **Role-Based Access Control (RBAC)** - Custom roles and permissions
- **User Session Tracking** - Login history and analytics
- **Multi-Tenant Ready** - Support for multiple organizations

---

## 🛠️ Tech Stack

### Backend
- **Framework:** Django 5.2.7
- **API:** Django REST Framework 3.x
- **Authentication:** JWT (djangorestframework-simplejwt)
- **Database:** SQLite (dev), PostgreSQL (production-ready)
- **CORS:** django-cors-headers
- **Filtering:** django-filter

### Frontend
- **Framework:** Vue 3 (Composition API)
- **Build Tool:** Vite 5
- **Styling:** Tailwind CSS 3
- **Router:** Vue Router 4
- **State Management:** Pinia
- **HTTP Client:** Axios with JWT interceptors
- **Forms:** VeeValidate + Yup
- **Charts:** Chart.js + vue-chartjs
- **UI Components:** Headless UI + Heroicons

### Architecture
- **Pattern:** SPA (Single-Page Application)
- **API Design:** RESTful with DRF ViewSets and Routers
- **Auth Flow:** JWT tokens with auto-refresh
- **State:** Pinia stores with centralized data management
- **Routing:** Client-side with Vue Router navigation guards

---

## 📁 Project Structure

```
datum/
├── backend/                          # Django backend
│   ├── datum_project/                # Main project settings
│   │   ├── settings.py               # Django + DRF + JWT config
│   │   └── urls.py                   # API routes
│   │
│   ├── geo/                          # Geography module (11 models)
│   │   ├── models.py                 # GlobalMarket, Country, Region, City, etc.
│   │   ├── serializers.py            # DRF serializers
│   │   ├── api_views.py              # ViewSets
│   │   ├── api_urls.py               # API endpoints
│   │   └── management/commands/
│   │       └── load_uzbekistan.py    # Uzbekistan data loader
│   │
│   ├── catalog/                      # Product catalog (7 models)
│   │   ├── models.py                 # Brand, Category, Product, EAV attributes
│   │   ├── serializers.py
│   │   ├── api_views.py
│   │   └── api_urls.py
│   │
│   ├── users/                        # User management (4 models)
│   │   ├── models.py                 # User, Role, Permission, Session
│   │   ├── serializers.py
│   │   ├── api_views.py
│   │   └── api_urls.py
│   │
│   ├── visits/                       # Mystery shopping visits (5 models)
│   ├── analytics/                    # Dashboards and metrics (5 models)
│   ├── coefficients/                 # Weighted KPIs (4 models)
│   ├── forms/                        # Dynamic form builder (1 model)
│   ├── integrations/                 # External APIs (3 models)
│   └── core/                         # Core utilities (4 models)
│
└── frontend/                         # Vue 3 SPA
    ├── src/
    │   ├── main.js                   # App entry point
    │   ├── App.vue                   # Root component
    │   ├── router/
    │   │   └── index.js              # Vue Router config
    │   ├── stores/
    │   │   ├── auth.js               # Auth store (JWT)
    │   │   └── geography.js          # Geography CRUD store
    │   ├── plugins/
    │   │   └── axios.js              # Axios + JWT interceptors
    │   ├── components/
    │   │   ├── layout/
    │   │   │   ├── Navbar.vue
    │   │   │   └── Sidebar.vue
    │   │   └── common/
    │   │       └── DataTable.vue     # Reusable CRUD table
    │   └── views/
    │       ├── Home.vue
    │       ├── auth/
    │       │   └── Login.vue
    │       └── geo/
    │           ├── CountryList.vue   # Full CRUD example
    │           └── ...
    │
    ├── package.json
    ├── vite.config.js
    ├── tailwind.config.js
    └── README.md                     # Frontend-specific docs
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.13.9
- Node.js 18+ and npm
- Git

### 1. Clone Repository

```bash
git clone https://github.com/maksad1git/datum.git
cd datum
```

### 2. Backend Setup

```bash
# Create and activate virtual environment
python -m venv venv_datum
./venv_datum/Scripts/activate      # Windows
source venv_datum/bin/activate     # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Install additional packages for API
pip install djangorestframework djangorestframework-simplejwt django-cors-headers django-filter

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Load Uzbekistan sample data (optional)
python manage.py load_uzbekistan

# Start Django server
python manage.py runserver
```

Backend will run at: **http://127.0.0.1:8000**

### 3. Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Copy environment config
cp .env.example .env

# Start Vite dev server
npm run dev
```

Frontend will run at: **http://localhost:5173**

### 4. Access the Application

- **Vue SPA:** http://localhost:5173
- **Django Admin:** http://127.0.0.1:8000/admin/
- **API Root:** http://127.0.0.1:8000/api/v1/
- **API Docs:** http://127.0.0.1:8000/api/v1/ (DRF Browsable API)

**Default credentials:** Create via Django admin or `createsuperuser` command

---

## 🔌 API Overview

### Authentication Endpoints
```
POST   /api/auth/token/              # Login (get JWT tokens)
POST   /api/auth/token/refresh/      # Refresh access token
```

### Geography API (11 endpoints)
```
GET/POST/PUT/DELETE   /api/v1/geo/globalmarkets/
GET/POST/PUT/DELETE   /api/v1/geo/countries/
GET/POST/PUT/DELETE   /api/v1/geo/regions/
GET/POST/PUT/DELETE   /api/v1/geo/cities/
GET/POST/PUT/DELETE   /api/v1/geo/districts/
GET/POST/PUT/DELETE   /api/v1/geo/channels/
GET/POST/PUT/DELETE   /api/v1/geo/outlets/
GET/POST/PUT/DELETE   /api/v1/geo/footfall-counters/
GET/POST/PUT/DELETE   /api/v1/geo/outlet-inventory/
GET/POST/PUT/DELETE   /api/v1/geo/displays/
GET/POST/PUT/DELETE   /api/v1/geo/display-inventory/
```

### Catalog API (7 endpoints)
```
GET/POST/PUT/DELETE   /api/v1/catalog/brands/
GET/POST/PUT/DELETE   /api/v1/catalog/categories/
GET/POST/PUT/DELETE   /api/v1/catalog/products/
GET/POST/PUT/DELETE   /api/v1/catalog/attribute-groups/
GET/POST/PUT/DELETE   /api/v1/catalog/attribute-definitions/
GET/POST/PUT/DELETE   /api/v1/catalog/product-attributes/
GET/POST/PUT/DELETE   /api/v1/catalog/category-templates/
```

### Users API (4 endpoints)
```
GET/POST/PUT/DELETE   /api/v1/users/roles/
GET/POST/PUT/DELETE   /api/v1/users/permissions/
GET/POST/PUT/DELETE   /api/v1/users/users/
GET/POST/PUT/DELETE   /api/v1/users/sessions/
```

All endpoints support:
- **Filtering:** `?field=value` (e.g., `?country=1`)
- **Search:** `?search=keyword`
- **Ordering:** `?ordering=field` or `?ordering=-field` (descending)
- **Pagination:** `?page=1&page_size=25`

---

## 📚 Documentation

- **[VUE_MIGRATION.md](VUE_MIGRATION.md)** - Complete Vue.js + Tailwind CSS migration guide
- **[frontend/README.md](frontend/README.md)** - Frontend-specific documentation
- **[HIERARCHY_MIGRATION_LOG.md](HIERARCHY_MIGRATION_LOG.md)** - Geographic hierarchy migration log

---

## 🗺️ Geographic Data

### Sample Data: Uzbekistan

The system includes a management command to load complete Uzbekistan geographic data:

```bash
python manage.py load_uzbekistan
```

This creates:
- **1 Country:** Uzbekistan
- **14 Regions:** Tashkent City, Andijan, Bukhara, Fergana, Jizzakh, Kashkadarya, Khorezm, Namangan, Navoi, Qashqadaryo, Samarkand, Sirdaryo, Surkhandarya, Tashkent Region
- **78 Cities**
- **58 Districts**

### Adding Your Own Data

1. **Via Django Admin:** http://127.0.0.1:8000/admin/
2. **Via API:** Use POST requests to `/api/v1/geo/*` endpoints
3. **Via Management Command:** Create custom commands in `geo/management/commands/`

---

## 🔧 Development

### Creating New API Endpoints

1. **Define Serializer** (`app/serializers.py`)
```python
class MyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyModel
        fields = '__all__'
```

2. **Create ViewSet** (`app/api_views.py`)
```python
class MyModelViewSet(viewsets.ModelViewSet):
    queryset = MyModel.objects.all()
    serializer_class = MyModelSerializer
    permission_classes = [IsAuthenticated]
```

3. **Register Router** (`app/api_urls.py`)
```python
router = DefaultRouter()
router.register(r'mymodels', MyModelViewSet, basename='mymodel')
urlpatterns = router.urls
```

4. **Include in Main URLs** (`datum_project/urls.py`)
```python
path('api/v1/myapp/', include('myapp.api_urls')),
```

### Creating Vue Components

See [frontend/README.md](frontend/README.md) for detailed Vue development guidelines.

---

## 📊 Migration Progress

**Current Status:** 40% Complete

- ✅ Django REST Framework + JWT setup
- ✅ Vue 3 + Tailwind CSS frontend scaffold
- ✅ Authentication flow with JWT
- ✅ 22 out of 44 models have REST API (50%)
- ✅ Reusable DataTable component
- ✅ CountryList full CRUD implementation
- ⏳ Remaining 22 models API (Visits, Analytics, Coefficients, Forms, Integrations, Core)
- ⏳ ~100+ Vue components for complete CRUD
- ⏳ Cascading select component for geo hierarchy
- ⏳ EAV attribute editor
- ⏳ Multi-level dashboards with Chart.js

See [VUE_MIGRATION.md](VUE_MIGRATION.md) for complete migration checklist and timeline.

---

## 🧪 Testing

### Backend Tests
```bash
python manage.py test
```

### Frontend Tests
```bash
cd frontend
npm run test
npm run test:e2e
```

---

## 📦 Production Deployment

### Backend
```bash
# Install production dependencies
pip install gunicorn psycopg2-binary

# Collect static files
python manage.py collectstatic

# Run with Gunicorn
gunicorn datum_project.wsgi:application --bind 0.0.0.0:8000
```

### Frontend
```bash
cd frontend
npm run build
# Deploy dist/ folder to static hosting (Netlify, Vercel, etc.)
```

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/my-feature`
3. Commit changes: `git commit -m "Add my feature"`
4. Push to branch: `git push origin feature/my-feature`
5. Open Pull Request

---

## 📄 License

This project is proprietary software for DATUM system.

---

## 👥 Authors

- **Maksad** - Initial work and Vue.js migration

---

## 🙏 Acknowledgments

- Django and DRF for powerful backend framework
- Vue.js team for reactive frontend framework
- Tailwind CSS for utility-first styling
- All contributors and testers

---

## 📧 Contact

- **Repository:** https://github.com/maksad1git/datum
- **Issues:** https://github.com/maksad1git/datum/issues

---

**Last Updated:** 2025-12-11
