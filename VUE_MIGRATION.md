# 🚀 Vue.js + Tailwind CSS SPA Migration Guide

## 📋 Migration Status

**Progress:** 40% Complete

### ✅ Completed

#### Backend (Django REST Framework)
- [x] DRF, django-cors-headers, django-filter, djangorestframework-simplejwt installed
- [x] REST Framework configured with JWT authentication
- [x] CORS configured for localhost:5173 (Vite dev server)
- [x] **GEO API** - 11 models (GlobalMarket, Country, Region, City, District, Channel, Outlet, FootfallCounter, OutletInventory, Display, DisplayInventory)
- [x] **CATALOG API** - 7 models (Brand, Category, Product, AttributeGroup, AttributeDefinition, ProductAttributeValue, CategoryAttributeTemplate)
- [x] **USERS API** - 4 models (User, Role, Permission, UserSession)
- [x] JWT endpoints: `/api/auth/token/`, `/api/auth/token/refresh/`

**Total:** 22 out of 44 models have REST API (50%)

#### Frontend (Vue 3 + Tailwind CSS)
- [x] Vue 3 project created with Vite
- [x] Tailwind CSS configured with custom theme
- [x] Vue Router with authentication guards
- [x] Pinia stores (auth, geography)
- [x] Axios with JWT interceptors and auto-refresh
- [x] Layout components (Navbar, Sidebar)
- [x] Authentication (Login page, JWT flow)
- [x] Home dashboard with stats
- [x] **DataTable** component (universal CRUD table)
- [x] **CountryList** - full CRUD implementation
- [x] 6 placeholder views for GEO entities

### ⏳ In Progress / Remaining

#### Backend API
- [ ] VISITS API (5 models)
- [ ] ANALYTICS API (5 models)
- [ ] COEFFICIENTS API (4 models)
- [ ] FORMS API (1 model)
- [ ] INTEGRATIONS API (3 models)
- [ ] CORE API (4 models)

#### Frontend Components
- [ ] Create/Edit forms for all entities (~44 forms)
- [ ] Detail views for all entities (~44 views)
- [ ] Remaining List views (~40 views)
- [ ] Cascading select component (for geo hierarchy)
- [ ] EAV attribute editor (for product attributes)
- [ ] Dynamic form builder (for visit forms)
- [ ] Multi-level dashboard with Chart.js
- [ ] File upload component
- [ ] Image gallery component
- [ ] PWA features (Service Worker, offline sync)

---

## 🏗️ Architecture

### Current Stack (Before Migration)
- **Backend:** Django 5.2.7 + Bootstrap 5 + jQuery
- **Frontend:** Server-side rendering (SSR) with Django templates
- **Routing:** Django URL patterns
- **State:** Session-based, no client-side state management

### New Stack (After Migration)
- **Backend:** Django 5.2.7 + Django REST Framework (API only)
- **Frontend:** Vue 3 + Vite + Tailwind CSS (SPA)
- **Routing:** Vue Router (client-side routing)
- **State:** Pinia (Vuex alternative)
- **Auth:** JWT tokens (localStorage + auto-refresh)
- **HTTP:** Axios with interceptors

---

## 📁 Project Structure

```
datum/
├── backend (Django)
│   ├── datum_project/          # Main project settings
│   ├── geo/                    # Geography app
│   │   ├── models.py
│   │   ├── serializers.py      # ✅ NEW
│   │   ├── api_views.py        # ✅ NEW
│   │   ├── api_urls.py         # ✅ NEW
│   │   ├── views.py            # 🟡 Legacy (to be deprecated)
│   │   └── urls.py             # 🟡 Legacy
│   ├── catalog/                # Catalog app
│   ├── users/                  # Users app
│   ├── visits/                 # Visits app
│   ├── analytics/              # Analytics app
│   └── ...
│
└── frontend/                   # ✅ NEW Vue 3 SPA
    ├── src/
    │   ├── main.js             # App entry point
    │   ├── App.vue             # Root component
    │   ├── router/
    │   │   └── index.js        # Vue Router config
    │   ├── stores/
    │   │   ├── auth.js         # Auth store (JWT)
    │   │   └── geography.js    # Geography store
    │   ├── plugins/
    │   │   └── axios.js        # Axios config with interceptors
    │   ├── components/
    │   │   ├── layout/
    │   │   │   ├── Navbar.vue
    │   │   │   └── Sidebar.vue
    │   │   └── common/
    │   │       └── DataTable.vue  # Reusable CRUD table
    │   └── views/
    │       ├── Home.vue
    │       ├── auth/
    │       │   └── Login.vue
    │       └── geo/
    │           ├── CountryList.vue
    │           ├── CountryDetail.vue
    │           └── ...
    ├── tailwind.config.js
    ├── vite.config.js
    └── package.json
```

---

## 🚀 Setup & Running

### Prerequisites
- Python 3.13.9
- Node.js 18+ and npm
- Git

### 1. Backend Setup

```bash
# Activate virtual environment
./venv_datum/Scripts/activate  # Windows
source venv_datum/bin/activate  # Linux/Mac

# Install dependencies (if not already)
pip install djangorestframework djangorestframework-simplejwt django-cors-headers django-filter

# Run migrations
python manage.py migrate

# Create superuser (if not exists)
python manage.py createsuperuser

# Load Uzbekistan data (optional)
python manage.py load_uzbekistan

# Start Django dev server
python manage.py runserver
```

Backend will run at: **http://127.0.0.1:8000**

### 2. Frontend Setup

```bash
# Navigate to frontend folder
cd frontend

# Install dependencies (if not already)
npm install

# Start Vite dev server
npm run dev
```

Frontend will run at: **http://localhost:5173**

### 3. Access the Application

- **Vue SPA:** http://localhost:5173
- **Django Admin:** http://127.0.0.1:8000/admin/
- **API Root:** http://127.0.0.1:8000/api/v1/
- **Legacy Django UI:** http://127.0.0.1:8000/ (still available)

**Default credentials:** `admin` / `admin` (or create via Django admin)

---

## 🔌 API Endpoints

### Authentication
```
POST /api/auth/token/          # Get JWT tokens
POST /api/auth/token/refresh/  # Refresh access token
```

### GEO API
```
GET    /api/v1/geo/globalmarkets/
GET    /api/v1/geo/countries/
GET    /api/v1/geo/regions/
GET    /api/v1/geo/cities/
GET    /api/v1/geo/districts/
GET    /api/v1/geo/channels/
GET    /api/v1/geo/outlets/
GET    /api/v1/geo/footfall-counters/
GET    /api/v1/geo/outlet-inventory/
GET    /api/v1/geo/displays/
GET    /api/v1/geo/display-inventory/
```

### CATALOG API
```
GET    /api/v1/catalog/brands/
GET    /api/v1/catalog/categories/
GET    /api/v1/catalog/products/
GET    /api/v1/catalog/attribute-groups/
GET    /api/v1/catalog/attribute-definitions/
GET    /api/v1/catalog/product-attributes/
GET    /api/v1/catalog/category-templates/
```

### USERS API
```
GET    /api/v1/users/roles/
GET    /api/v1/users/permissions/
GET    /api/v1/users/users/
GET    /api/v1/users/sessions/
```

All endpoints support: `GET`, `POST`, `PUT`, `PATCH`, `DELETE`

---

## 🎨 Frontend Features

### 1. Authentication Flow
- Login page with JWT authentication
- Auto-refresh expired tokens (interceptor)
- Protected routes with navigation guards
- Logout with token cleanup

### 2. DataTable Component
**Location:** `frontend/src/components/common/DataTable.vue`

**Features:**
- Search functionality
- Pagination
- Custom cell templates (slots)
- Edit/Delete actions
- Loading/Error states
- Responsive design

**Usage:**
```vue
<DataTable
  :data="items"
  :columns="[
    { key: 'name', label: 'Name' },
    { key: 'code', label: 'Code' }
  ]"
  :loading="loading"
  :error="error"
  @edit="handleEdit"
  @delete="handleDelete"
>
  <template #cell-name="{ item }">
    <router-link :to="`/items/${item.id}`">
      {{ item.name }}
    </router-link>
  </template>
</DataTable>
```

### 3. Pinia Stores

#### Auth Store
**Location:** `frontend/src/stores/auth.js`

```javascript
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

// Login
await authStore.login(username, password)

// Check authentication
if (authStore.isAuthenticated) { }

// Logout
authStore.logout()
```

#### Geography Store
**Location:** `frontend/src/stores/geography.js`

```javascript
import { useGeographyStore } from '@/stores/geography'

const geo = useGeographyStore()

// Fetch data
await geo.fetchCountries()
await geo.fetchCities({ region: regionId })

// CRUD operations
await geo.createCountry(data)
await geo.updateCountry(id, data)
await geo.deleteCountry(id)
```

---

## 🔧 Development Guidelines

### Creating New API Endpoints

1. **Create Serializers** (`app/serializers.py`)
```python
from rest_framework import serializers
from .models import MyModel

class MyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyModel
        fields = '__all__'
```

2. **Create ViewSets** (`app/api_views.py`)
```python
from rest_framework import viewsets
from .models import MyModel
from .serializers import MyModelSerializer

class MyModelViewSet(viewsets.ModelViewSet):
    queryset = MyModel.objects.all()
    serializer_class = MyModelSerializer
    permission_classes = [IsAuthenticated]
```

3. **Create Router** (`app/api_urls.py`)
```python
from rest_framework.routers import DefaultRouter
from .api_views import MyModelViewSet

router = DefaultRouter()
router.register(r'mymodels', MyModelViewSet, basename='mymodel')
urlpatterns = router.urls
```

4. **Register in main URLs** (`datum_project/urls.py`)
```python
path('api/v1/myapp/', include('myapp.api_urls')),
```

### Creating New Vue Components

1. **Create View** (`frontend/src/views/myapp/MyModelList.vue`)
2. **Add Route** (`frontend/src/router/index.js`)
3. **Create Pinia Store** (if needed) (`frontend/src/stores/myapp.js`)
4. **Use DataTable component** for list views

---

## 📝 Migration Checklist

### Per Django App (9 apps total)

- [ ] **GEO** - ✅ DONE
  - [x] Serializers (11)
  - [x] ViewSets (11)
  - [x] URLs
  - [x] Vue store
  - [x] Vue components (1 complete, 6 placeholders)

- [ ] **CATALOG** - 🟡 IN PROGRESS
  - [x] Serializers (7)
  - [x] ViewSets (7)
  - [x] URLs
  - [ ] Vue store
  - [ ] Vue components

- [ ] **USERS** - 🟡 IN PROGRESS
  - [x] Serializers (4)
  - [x] ViewSets (4)
  - [x] URLs
  - [ ] Vue store
  - [ ] Vue components

- [ ] **VISITS** - ⏳ TODO
- [ ] **ANALYTICS** - ⏳ TODO
- [ ] **COEFFICIENTS** - ⏳ TODO
- [ ] **FORMS** - ⏳ TODO
- [ ] **INTEGRATIONS** - ⏳ TODO
- [ ] **CORE** - ⏳ TODO

---

## 🐛 Known Issues

1. **CSRF Tokens:** JWT replaces CSRF, but legacy views still use CSRF
2. **File Uploads:** Need to implement multipart/form-data handling in Vue
3. **PWA Features:** Service Worker not yet migrated from Django templates
4. **Cascading Selects:** Geo hierarchy dropdowns need Vue implementation

---

## 📊 Estimated Timeline

**Completed:** Phases 1-3 (3 weeks)
**Remaining:**
- Phase 4: Remaining APIs (2 weeks)
- Phase 5: Vue components expansion (4 weeks)
- Phase 6: Complex features (cascading, EAV, dashboards) (3 weeks)
- Phase 7: Testing & bug fixes (2 weeks)
- Phase 8: Deprecate Django templates (1 week)

**Total:** ~15 weeks for full migration

---

## 🎯 Next Steps

1. **Complete remaining API endpoints** (Visits, Analytics, Coefficients, Forms, Integrations, Core)
2. **Create Pinia stores** for remaining apps
3. **Implement Create/Edit forms** using VeeValidate
4. **Build cascading select component** for geo hierarchy
5. **Implement EAV attribute editor** for products
6. **Create dashboard** with Chart.js integration
7. **Add file upload** support
8. **Implement PWA features** (Service Worker, offline mode)
9. **Write tests** for Vue components
10. **Deploy** to production

---

## 📚 Resources

- **Django REST Framework:** https://www.django-rest-framework.org/
- **Vue 3 Docs:** https://vuejs.org/
- **Tailwind CSS:** https://tailwindcss.com/
- **Pinia:** https://pinia.vuejs.org/
- **Vite:** https://vitejs.dev/

---

**Repository:** https://github.com/maksad1git/datum
**Last Updated:** 2025-12-11
