<template>
  <div class="min-h-screen bg-gray-50">
    <Navbar />

    <div class="flex">
      <Sidebar />

      <main class="flex-1 p-8 ml-64">
        <div class="max-w-7xl mx-auto">
          <!-- Header -->
          <div class="flex justify-between items-center mb-6">
            <h1 class="text-3xl font-bold text-gray-900">Preinstalled Products</h1>
            <button
              @click="handleCreate"
              class="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-lg shadow-md transition duration-200"
            >
              + Add Preinstall
            </button>
          </div>

          <!-- Filters -->
          <div class="bg-white rounded-lg shadow-md p-4 mb-6">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Product</label>
                <select
                  v-model="filters.product"
                  @change="applyFilters"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="">All Products</option>
                  <option v-for="product in catalogStore.products" :key="product.id" :value="product.id">
                    {{ product.name }}
                  </option>
                </select>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Outlet</label>
                <input
                  type="text"
                  v-model="filters.outlet_search"
                  @input="applyFilters"
                  placeholder="Search outlet..."
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
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
            :data="catalogStore.preinstalls"
            :columns="columns"
            :loading="catalogStore.preinstallsLoading"
            :error="catalogStore.preinstallsError"
            empty-message="No preinstalled products found"
            @edit="handleEdit"
            @delete="handleDelete"
          >
            <template #cell-product_name="{ item }">
              <router-link
                v-if="item.product"
                :to="`/catalog/products/${item.product}`"
                class="text-blue-600 hover:text-blue-800 font-medium"
              >
                {{ item.product_name || `Product #${item.product}` }}
              </router-link>
              <span v-else class="text-gray-400">N/A</span>
            </template>

            <template #cell-outlet_name="{ item }">
              <router-link
                v-if="item.outlet"
                :to="`/geo/outlets/${item.outlet}`"
                class="text-blue-600 hover:text-blue-800"
              >
                {{ item.outlet_name || `Outlet #${item.outlet}` }}
              </router-link>
              <span v-else class="text-gray-400">N/A</span>
            </template>

            <template #cell-install_date="{ item }">
              <span class="text-gray-700">{{ formatDate(item.install_date) }}</span>
            </template>

            <template #cell-quantity="{ item }">
              <span class="font-semibold text-gray-900">{{ item.quantity || 0 }}</span>
            </template>

            <template #cell-expected_sales="{ item }">
              <span v-if="item.expected_sales" class="text-gray-700">{{ item.expected_sales }}</span>
              <span v-else class="text-gray-400 text-sm italic">Not set</span>
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

            <template #cell-notes="{ item }">
              <span v-if="item.notes" class="text-gray-600 text-sm truncate max-w-xs">
                {{ item.notes }}
              </span>
              <span v-else class="text-gray-400 text-sm italic">No notes</span>
            </template>
          </DataTable>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useCatalogStore } from '@/stores/catalog'
import Navbar from '@/components/layout/Navbar.vue'
import Sidebar from '@/components/layout/Sidebar.vue'
import DataTable from '@/components/common/DataTable.vue'

const router = useRouter()
const catalogStore = useCatalogStore()

const columns = ref([
  { key: 'product_name', label: 'Product' },
  { key: 'outlet_name', label: 'Outlet' },
  { key: 'install_date', label: 'Install Date' },
  { key: 'quantity', label: 'Quantity' },
  { key: 'expected_sales', label: 'Expected Sales' },
  { key: 'is_active', label: 'Status' },
  { key: 'notes', label: 'Notes' }
])

const filters = ref({
  product: '',
  outlet_search: '',
  is_active: ''
})

const formatDate = (date) => {
  if (!date) return 'N/A'
  return new Date(date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

const handleCreate = () => {
  router.push('/catalog/preinstalls/create')
}

const handleEdit = (preinstall) => {
  router.push(`/catalog/preinstalls/${preinstall.id}/edit`)
}

const handleDelete = async (preinstall) => {
  if (confirm(`Delete preinstall record? This action cannot be undone.`)) {
    try {
      await catalogStore.deletePreinstall(preinstall.id)
      alert('Preinstall deleted successfully')
    } catch (error) {
      alert('Failed to delete preinstall: ' + (error.response?.data?.detail || error.message))
    }
  }
}

const applyFilters = async () => {
  const params = {}
  if (filters.value.product) params.product = filters.value.product
  if (filters.value.outlet_search) params.outlet__name__icontains = filters.value.outlet_search
  if (filters.value.is_active !== '') params.is_active = filters.value.is_active

  await catalogStore.fetchPreinstalls(params)
}

onMounted(async () => {
  await Promise.all([
    catalogStore.fetchPreinstalls(),
    catalogStore.fetchProducts()
  ])
})
</script>
