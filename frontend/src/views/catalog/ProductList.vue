<template>
  <div class="min-h-screen bg-gray-50">
    <Navbar />

    <div class="flex">
      <Sidebar />

      <main class="flex-1 p-8 ml-64">
        <div class="max-w-7xl mx-auto">
          <!-- Header -->
          <div class="flex justify-between items-center mb-6">
            <h1 class="text-3xl font-bold text-gray-900">Products</h1>
            <button
              @click="handleCreate"
              class="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-lg shadow-md transition duration-200"
            >
              + Create Product
            </button>
          </div>

          <!-- Filters -->
          <div class="bg-white rounded-lg shadow-md p-4 mb-6">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Brand</label>
                <select
                  v-model="filters.brand"
                  @change="applyFilters"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="">All Brands</option>
                  <option v-for="brand in catalogStore.brands" :key="brand.id" :value="brand.id">
                    {{ brand.name }}
                  </option>
                </select>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Category</label>
                <select
                  v-model="filters.category"
                  @change="applyFilters"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="">All Categories</option>
                  <option v-for="category in catalogStore.categories" :key="category.id" :value="category.id">
                    {{ category.name }}
                  </option>
                </select>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Status</label>
                <select
                  v-model="filters.is_active"
                  @change="applyFilters"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="">All</option>
                  <option value="true">Active</option>
                  <option value="false">Inactive</option>
                </select>
              </div>
            </div>
          </div>

          <!-- DataTable -->
          <DataTable
            :data="filteredProducts"
            :columns="columns"
            :loading="catalogStore.productsLoading"
            :error="catalogStore.productsError"
            empty-message="No products found"
            @edit="handleEdit"
            @delete="handleDelete"
          >
            <template #cell-image="{ item }">
              <img
                v-if="item.image"
                :src="item.image"
                :alt="item.name"
                class="h-10 w-10 rounded object-cover"
              />
              <span v-else class="text-gray-400 text-sm">No image</span>
            </template>

            <template #cell-name="{ item }">
              <router-link
                :to="`/catalog/products/${item.id}`"
                class="text-blue-600 hover:text-blue-800 font-medium"
              >
                {{ item.name }}
              </router-link>
            </template>

            <template #cell-code="{ item }">
              <code class="bg-gray-100 px-2 py-1 rounded text-sm">{{ item.code }}</code>
            </template>

            <template #cell-brand_name="{ item }">
              <span class="text-gray-700">{{ item.brand_name || 'N/A' }}</span>
            </template>

            <template #cell-category_name="{ item }">
              <span class="text-gray-700">{{ item.category_name || 'N/A' }}</span>
            </template>

            <template #cell-price="{ item }">
              <span v-if="item.price" class="font-medium text-gray-900">
                {{ formatPrice(item.price) }}
              </span>
              <span v-else class="text-gray-400">-</span>
            </template>

            <template #cell-is_active="{ item }">
              <span
                class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full"
                :class="{
                  'bg-green-100 text-green-800': item.is_active,
                  'bg-red-100 text-red-800': !item.is_active
                }"
              >
                {{ item.is_active ? 'Active' : 'Inactive' }}
              </span>
            </template>
          </DataTable>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useCatalogStore } from '@/stores/catalog'
import Navbar from '@/components/layout/Navbar.vue'
import Sidebar from '@/components/layout/Sidebar.vue'
import DataTable from '@/components/common/DataTable.vue'

const router = useRouter()
const catalogStore = useCatalogStore()

const columns = ref([
  { key: 'image', label: 'Image' },
  { key: 'name', label: 'Name' },
  { key: 'code', label: 'Code' },
  { key: 'brand_name', label: 'Brand' },
  { key: 'category_name', label: 'Category' },
  { key: 'price', label: 'Price' },
  { key: 'is_active', label: 'Status' }
])

const filters = ref({
  brand: '',
  category: '',
  is_active: ''
})

const filteredProducts = computed(() => {
  let products = catalogStore.products

  if (filters.value.brand) {
    products = products.filter(p => p.brand === parseInt(filters.value.brand))
  }

  if (filters.value.category) {
    products = products.filter(p => p.category === parseInt(filters.value.category))
  }

  if (filters.value.is_active !== '') {
    const isActive = filters.value.is_active === 'true'
    products = products.filter(p => p.is_active === isActive)
  }

  return products
})

const formatPrice = (price) => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD'
  }).format(price)
}

const handleCreate = () => {
  router.push('/catalog/products/create')
}

const handleEdit = (product) => {
  router.push(`/catalog/products/${product.id}/edit`)
}

const handleDelete = async (product) => {
  if (confirm(`Delete product "${product.name}"? This action cannot be undone.`)) {
    try {
      await catalogStore.deleteProduct(product.id)
      alert('Product deleted successfully')
    } catch (error) {
      alert('Failed to delete product: ' + (error.response?.data?.detail || error.message))
    }
  }
}

const applyFilters = async () => {
  const params = {}
  if (filters.value.brand) params.brand = filters.value.brand
  if (filters.value.category) params.category = filters.value.category
  if (filters.value.is_active !== '') params.is_active = filters.value.is_active

  await catalogStore.fetchProducts(params)
}

onMounted(async () => {
  await Promise.all([
    catalogStore.fetchProducts(),
    catalogStore.fetchBrands(),
    catalogStore.fetchCategories()
  ])
})
</script>
