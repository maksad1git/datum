<template>
  <aside class="fixed top-16 left-0 h-[calc(100vh-4rem)] w-64 bg-white shadow-lg overflow-y-auto">
    <nav class="p-4">
      <div class="space-y-1">
        <!-- Home -->
        <router-link
          to="/"
          class="flex items-center px-4 py-2 text-sm font-medium rounded-md transition"
          :class="isActive('/') ? 'bg-primary text-white' : 'text-gray-700 hover:bg-gray-100'"
        >
          <svg class="mr-3 h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
          </svg>
          Dashboard
        </router-link>

        <!-- Geography Section -->
        <div class="pt-4">
          <h3 class="px-4 text-xs font-semibold text-gray-500 uppercase tracking-wider">
            Geography
          </h3>
          <div class="mt-2 space-y-1">
            <router-link
              to="/geo/countries"
              class="flex items-center px-4 py-2 text-sm font-medium rounded-md transition"
              :class="isActive('/geo/countries') ? 'bg-primary text-white' : 'text-gray-700 hover:bg-gray-100'"
            >
              Countries
            </router-link>
            <router-link
              to="/geo/regions"
              class="flex items-center px-4 py-2 text-sm font-medium rounded-md transition"
              :class="isActive('/geo/regions') ? 'bg-primary text-white' : 'text-gray-700 hover:bg-gray-100'"
            >
              Regions
            </router-link>
            <router-link
              to="/geo/cities"
              class="flex items-center px-4 py-2 text-sm font-medium rounded-md transition"
              :class="isActive('/geo/cities') ? 'bg-primary text-white' : 'text-gray-700 hover:bg-gray-100'"
            >
              Cities
            </router-link>
            <router-link
              to="/geo/districts"
              class="flex items-center px-4 py-2 text-sm font-medium rounded-md transition"
              :class="isActive('/geo/districts') ? 'bg-primary text-white' : 'text-gray-700 hover:bg-gray-100'"
            >
              Districts
            </router-link>
            <router-link
              to="/geo/channels"
              class="flex items-center px-4 py-2 text-sm font-medium rounded-md transition"
              :class="isActive('/geo/channels') ? 'bg-primary text-white' : 'text-gray-700 hover:bg-gray-100'"
            >
              Channels
            </router-link>
            <router-link
              to="/geo/outlets"
              class="flex items-center px-4 py-2 text-sm font-medium rounded-md transition"
              :class="isActive('/geo/outlets') ? 'bg-primary text-white' : 'text-gray-700 hover:bg-gray-100'"
            >
              Outlets
            </router-link>
          </div>
        </div>

        <!-- Catalog Section -->
        <div class="pt-4">
          <h3 class="px-4 text-xs font-semibold text-gray-500 uppercase tracking-wider">
            Catalog
          </h3>
          <div class="mt-2 space-y-1">
            <router-link
              to="/catalog/brands"
              class="flex items-center px-4 py-2 text-sm font-medium rounded-md transition"
              :class="isActive('/catalog/brands') ? 'bg-primary text-white' : 'text-gray-700 hover:bg-gray-100'"
            >
              Brands
            </router-link>
            <router-link
              to="/catalog/categories"
              class="flex items-center px-4 py-2 text-sm font-medium rounded-md transition"
              :class="isActive('/catalog/categories') ? 'bg-primary text-white' : 'text-gray-700 hover:bg-gray-100'"
            >
              Categories
            </router-link>
            <router-link
              to="/catalog/products"
              class="flex items-center px-4 py-2 text-sm font-medium rounded-md transition"
              :class="isActive('/catalog/products') ? 'bg-primary text-white' : 'text-gray-700 hover:bg-gray-100'"
            >
              Products
            </router-link>
            <router-link
              to="/catalog/preinstalls"
              class="flex items-center px-4 py-2 text-sm font-medium rounded-md transition"
              :class="isActive('/catalog/preinstalls') ? 'bg-primary text-white' : 'text-gray-700 hover:bg-gray-100'"
            >
              Preinstalls
            </router-link>
          </div>
        </div>

        <!-- Visits Section -->
        <div class="pt-4">
          <h3 class="px-4 text-xs font-semibold text-gray-500 uppercase tracking-wider">
            Visits
          </h3>
          <div class="mt-2 space-y-1">
            <router-link
              to="/visits/visit-types"
              class="flex items-center px-4 py-2 text-sm font-medium rounded-md transition"
              :class="isActive('/visits/visit-types') ? 'bg-primary text-white' : 'text-gray-700 hover:bg-gray-100'"
            >
              Visit Types
            </router-link>
            <router-link
              to="/visits/visits"
              class="flex items-center px-4 py-2 text-sm font-medium rounded-md transition"
              :class="isActive('/visits/visits') ? 'bg-primary text-white' : 'text-gray-700 hover:bg-gray-100'"
            >
              Visits
            </router-link>
            <router-link
              to="/visits/observations"
              class="flex items-center px-4 py-2 text-sm font-medium rounded-md transition"
              :class="isActive('/visits/observations') ? 'bg-primary text-white' : 'text-gray-700 hover:bg-gray-100'"
            >
              Observations
            </router-link>
            <router-link
              to="/visits/sales"
              class="flex items-center px-4 py-2 text-sm font-medium rounded-md transition"
              :class="isActive('/visits/sales') ? 'bg-primary text-white' : 'text-gray-700 hover:bg-gray-100'"
            >
              Sales
            </router-link>
          </div>
        </div>
      </div>
    </nav>
  </aside>
</template>

<script setup>
import { useRoute } from 'vue-router'

const route = useRoute()

const isActive = (path) => {
  if (path === '/') {
    return route.path === '/'
  }
  return route.path.startsWith(path)
}
</script>
