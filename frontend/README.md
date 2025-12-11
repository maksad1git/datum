# DATUM Frontend - Vue 3 + Tailwind CSS SPA

Modern Single-Page Application for the DATUM mystery shopping and data collection system.

## 🛠️ Tech Stack

- **Framework:** Vue 3 (Composition API)
- **Build Tool:** Vite 5
- **Styling:** Tailwind CSS 3
- **Router:** Vue Router 4
- **State Management:** Pinia
- **HTTP Client:** Axios
- **Forms:** VeeValidate + Yup
- **Charts:** Chart.js + vue-chartjs
- **UI Components:** Headless UI + Heroicons

## 📦 Installation

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## 🚀 Development Server

```bash
npm run dev
```

Frontend runs at: **http://localhost:5173**

## 🔑 Environment Variables

Create a `.env` file in the frontend directory:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
VITE_API_VERSION=v1
```

## 📁 Project Structure

```
frontend/
├── src/
│   ├── main.js                 # App entry point
│   ├── App.vue                 # Root component
│   ├── style.css               # Global styles + Tailwind
│   │
│   ├── router/
│   │   └── index.js            # Vue Router configuration
│   │
│   ├── stores/                 # Pinia stores
│   │   ├── auth.js             # Authentication store
│   │   └── geography.js        # Geography CRUD store
│   │
│   ├── plugins/
│   │   └── axios.js            # Axios config + interceptors
│   │
│   ├── components/
│   │   ├── layout/             # Layout components
│   │   │   ├── Navbar.vue
│   │   │   └── Sidebar.vue
│   │   └── common/             # Reusable components
│   │       └── DataTable.vue   # Universal CRUD table
│   │
│   └── views/                  # Page components
│       ├── Home.vue
│       ├── auth/
│       │   └── Login.vue
│       └── geo/
│           ├── CountryList.vue
│           └── ...
│
├── public/                     # Static assets
├── index.html                  # HTML entry point
├── package.json
├── vite.config.js
├── tailwind.config.js
└── postcss.config.js
```

## 🎨 Component Conventions

### Page Components (Views)

Located in `src/views/`, page components follow this structure:

```vue
<template>
  <div class="min-h-screen bg-gray-50">
    <Navbar />
    <div class="flex">
      <Sidebar />
      <main class="flex-1 p-8 ml-64">
        <!-- Page content -->
      </main>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import Navbar from '@/components/layout/Navbar.vue'
import Sidebar from '@/components/layout/Sidebar.vue'

onMounted(() => {
  // Fetch data
})
</script>
```

### Reusable Components

Located in `src/components/`, use Composition API with `<script setup>`:

```vue
<template>
  <!-- Component template -->
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  // Props
})

const emit = defineEmits(['event-name'])
</script>
```

## 🔐 Authentication

### Login Flow

```javascript
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

// Login
await authStore.login(username, password)

// Check if authenticated
if (authStore.isAuthenticated) {
  // User is logged in
}

// Get current user
const user = authStore.user

// Logout
authStore.logout()
```

### Protected Routes

Routes with `meta: { requiresAuth: true }` require authentication:

```javascript
{
  path: '/dashboard',
  component: Dashboard,
  meta: { requiresAuth: true }
}
```

### API Calls with JWT

Axios is pre-configured with JWT interceptors:

```javascript
import axios from 'axios'

// Token is automatically added to headers
const response = await axios.get('/api/v1/geo/countries/')

// Expired tokens are automatically refreshed
```

## 📊 State Management (Pinia)

### Creating a Store

```javascript
import { defineStore } from 'pinia'
import axios from 'axios'

export const useMyStore = defineStore('myStore', {
  state: () => ({
    items: [],
    loading: false,
    error: null
  }),

  getters: {
    itemCount: (state) => state.items.length
  },

  actions: {
    async fetchItems() {
      this.loading = true
      try {
        const response = await axios.get('/api/v1/items/')
        this.items = response.data.results || response.data
      } catch (error) {
        this.error = error.message
      } finally {
        this.loading = false
      }
    }
  }
})
```

### Using a Store

```vue
<script setup>
import { useMyStore } from '@/stores/myStore'

const myStore = useMyStore()

// Access state
console.log(myStore.items)

// Call actions
await myStore.fetchItems()

// Use getters
console.log(myStore.itemCount)
</script>
```

## 🔄 DataTable Component

Universal CRUD table component with search, pagination, and custom slots.

### Basic Usage

```vue
<template>
  <DataTable
    :data="items"
    :columns="columns"
    :loading="loading"
    :error="error"
    @edit="handleEdit"
    @delete="handleDelete"
  />
</template>

<script setup>
import { ref } from 'vue'
import DataTable from '@/components/common/DataTable.vue'

const columns = ref([
  { key: 'name', label: 'Name' },
  { key: 'code', label: 'Code' }
])

const handleEdit = (item) => {
  // Handle edit
}

const handleDelete = async (item) => {
  // Handle delete
}
</script>
```

### Custom Cell Templates

```vue
<DataTable :data="items" :columns="columns">
  <template #cell-name="{ item }">
    <router-link :to="`/items/${item.id}`">
      {{ item.name }}
    </router-link>
  </template>

  <template #cell-status="{ item }">
    <span :class="getStatusClass(item.status)">
      {{ item.status }}
    </span>
  </template>
</DataTable>
```

### Props

- `data` (Array, required) - Array of items to display
- `columns` (Array, required) - Column definitions `[{ key: 'name', label: 'Name' }]`
- `loading` (Boolean) - Show loading state
- `error` (String) - Error message to display
- `emptyMessage` (String) - Message when no data
- `showActions` (Boolean, default: true) - Show edit/delete buttons

### Events

- `@edit` - Emitted when edit button clicked
- `@delete` - Emitted when delete button clicked
- `@page-change` - Emitted when page changes

## 🎨 Tailwind CSS Utilities

### Custom Colors (DATUM Brand)

```css
text-primary      /* #0d6efd - Blue */
text-success      /* #198754 - Green */
text-danger       /* #dc3545 - Red */
text-warning      /* #ffc107 - Yellow */
text-info         /* #0dcaf0 - Cyan */
```

### Common Button Styles

```vue
<button class="btn btn-primary">Primary</button>
<button class="btn btn-success">Success</button>
<button class="btn btn-danger">Danger</button>
```

### Card Component

```vue
<div class="bg-white rounded-lg shadow-lg p-6">
  <!-- Card content -->
</div>
```

## 🧪 Testing

```bash
# Run unit tests
npm run test

# Run E2E tests
npm run test:e2e
```

## 📦 Building for Production

```bash
# Create production build
npm run build

# Preview build locally
npm run preview
```

Build output will be in the `dist/` directory.

## 🔧 Vite Configuration

See [vite.config.js](vite.config.js) for build configuration.

Key features:
- Path aliases (`@/` = `src/`)
- Auto-import Vue components
- Optimized build settings

## 🐛 Common Issues

### CORS Errors

Make sure Django backend has CORS configured:

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
```

### 401 Unauthorized

Check that JWT tokens are valid:
1. Login again to refresh tokens
2. Check `localStorage` for `access_token` and `refresh_token`
3. Verify Django JWT settings

### Hot Module Replacement (HMR) Not Working

1. Check Vite dev server is running
2. Clear browser cache
3. Restart Vite server: `npm run dev`

## 📚 Resources

- [Vue 3 Documentation](https://vuejs.org/)
- [Vite Documentation](https://vitejs.dev/)
- [Tailwind CSS Documentation](https://tailwindcss.com/)
- [Pinia Documentation](https://pinia.vuejs.org/)
- [Vue Router Documentation](https://router.vuejs.org/)
- [VeeValidate Documentation](https://vee-validate.logaretm.com/)

## 👥 Contributing

1. Create feature branch: `git checkout -b feature/my-feature`
2. Commit changes: `git commit -m "Add my feature"`
3. Push to branch: `git push origin feature/my-feature`
4. Open Pull Request

## 📄 License

This project is part of the DATUM system.

---

**Last Updated:** 2025-12-11
