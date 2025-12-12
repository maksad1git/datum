<template>
  <div class="min-h-screen bg-gray-50">
    <Navbar />

    <div class="flex">
      <Sidebar />

      <main class="flex-1 p-8 ml-64">
        <div class="max-w-7xl mx-auto">
          <!-- Header -->
          <div class="flex justify-between items-center mb-6">
            <h1 class="text-3xl font-bold text-gray-900">Sales Data</h1>
          </div>

          <!-- Filters -->
          <div class="bg-white rounded-lg shadow-md p-4 mb-6">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
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
                <label class="block text-sm font-medium text-gray-700 mb-2">Date From</label>
                <input
                  type="date"
                  v-model="filters.date_from"
                  @change="applyFilters"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Date To</label>
                <input
                  type="date"
                  v-model="filters.date_to"
                  @change="applyFilters"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
            </div>
          </div>

          <!-- Stats Cards -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
            <div class="bg-white rounded-lg shadow-md p-6">
              <div class="flex items-center">
                <div class="flex-shrink-0 bg-blue-500 rounded-md p-3">
                  <svg class="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <div class="ml-5">
                  <p class="text-sm font-medium text-gray-500">Total Sales</p>
                  <p class="text-2xl font-bold text-gray-900">{{ totalSales }}</p>
                </div>
              </div>
            </div>

            <div class="bg-white rounded-lg shadow-md p-6">
              <div class="flex items-center">
                <div class="flex-shrink-0 bg-green-500 rounded-md p-3">
                  <svg class="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
                  </svg>
                </div>
                <div class="ml-5">
                  <p class="text-sm font-medium text-gray-500">Total Revenue</p>
                  <p class="text-2xl font-bold text-gray-900">${{ totalRevenue.toFixed(2) }}</p>
                </div>
              </div>
            </div>

            <div class="bg-white rounded-lg shadow-md p-6">
              <div class="flex items-center">
                <div class="flex-shrink-0 bg-purple-500 rounded-md p-3">
                  <svg class="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
                  </svg>
                </div>
                <div class="ml-5">
                  <p class="text-sm font-medium text-gray-500">Avg Price</p>
                  <p class="text-2xl font-bold text-gray-900">${{ avgPrice.toFixed(2) }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- DataTable -->
          <DataTable
            :data="visitsStore.sales"
            :columns="columns"
            :loading="visitsStore.salesLoading"
            :error="visitsStore.salesError"
            empty-message="No sales data found"
            @edit="handleEdit"
            @delete="handleDelete"
          >
            <template #cell-outlet_name="{ item }">
              <router-link
                v-if="item.outlet"
                :to="`/geo/outlets/${item.outlet}`"
                class="text-blue-600 hover:text-blue-800 font-medium"
              >
                {{ item.outlet_name || `Outlet #${item.outlet}` }}
              </router-link>
              <span v-else class="text-gray-400">N/A</span>
            </template>

            <template #cell-product_name="{ item }">
              <router-link
                v-if="item.product"
                :to="`/catalog/products/${item.product}`"
                class="text-blue-600 hover:text-blue-800"
              >
                {{ item.product_name || `Product #${item.product}` }}
              </router-link>
              <span v-else class="text-gray-400">N/A</span>
            </template>

            <template #cell-sale_date="{ item }">
              <span class="text-gray-700">{{ formatDate(item.sale_date) }}</span>
            </template>

            <template #cell-quantity="{ item }">
              <span class="font-semibold text-gray-900">{{ item.quantity || 0 }}</span>
            </template>

            <template #cell-unit_price="{ item }">
              <span class="text-gray-700">${{ item.unit_price ? item.unit_price.toFixed(2) : '0.00' }}</span>
            </template>

            <template #cell-total_amount="{ item }">
              <span class="font-bold text-green-700">${{ item.total_amount ? item.total_amount.toFixed(2) : '0.00' }}</span>
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
import { useVisitsStore } from '@/stores/visits'
import Navbar from '@/components/layout/Navbar.vue'
import Sidebar from '@/components/layout/Sidebar.vue'
import DataTable from '@/components/common/DataTable.vue'

const router = useRouter()
const visitsStore = useVisitsStore()

const columns = ref([
  { key: 'outlet_name', label: 'Outlet' },
  { key: 'product_name', label: 'Product' },
  { key: 'sale_date', label: 'Sale Date' },
  { key: 'quantity', label: 'Qty' },
  { key: 'unit_price', label: 'Unit Price' },
  { key: 'total_amount', label: 'Total' }
])

const filters = ref({
  outlet_search: '',
  date_from: '',
  date_to: ''
})

const totalSales = computed(() => {
  return visitsStore.sales.reduce((sum, sale) => sum + (sale.quantity || 0), 0)
})

const totalRevenue = computed(() => {
  return visitsStore.sales.reduce((sum, sale) => sum + (sale.total_amount || 0), 0)
})

const avgPrice = computed(() => {
  if (visitsStore.sales.length === 0) return 0
  return totalRevenue.value / totalSales.value
})

const formatDate = (date) => {
  if (!date) return 'N/A'
  return new Date(date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

const handleEdit = (sale) => {
  router.push(`/visits/sales/${sale.id}/edit`)
}

const handleDelete = async (sale) => {
  if (confirm(`Delete sale record? This action cannot be undone.`)) {
    try {
      await visitsStore.deleteSale(sale.id)
      alert('Sale deleted successfully')
    } catch (error) {
      alert('Failed to delete sale: ' + (error.response?.data?.detail || error.message))
    }
  }
}

const applyFilters = async () => {
  const params = {}
  if (filters.value.outlet_search) params.outlet__name__icontains = filters.value.outlet_search
  if (filters.value.date_from) params.sale_date_after = filters.value.date_from
  if (filters.value.date_to) params.sale_date_before = filters.value.date_to

  await visitsStore.fetchSales(params)
}

onMounted(async () => {
  await visitsStore.fetchSales()
})
</script>
