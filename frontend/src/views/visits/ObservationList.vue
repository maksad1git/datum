<template>
  <div class="min-h-screen bg-gray-50">
    <Navbar />

    <div class="flex">
      <Sidebar />

      <main class="flex-1 p-8 ml-64">
        <div class="max-w-7xl mx-auto">
          <!-- Header -->
          <div class="flex justify-between items-center mb-6">
            <h1 class="text-3xl font-bold text-gray-900">Visit Observations</h1>
          </div>

          <!-- Filters -->
          <div class="bg-white rounded-lg shadow-md p-4 mb-6">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Visit ID</label>
                <input
                  type="number"
                  v-model="filters.visit"
                  @input="applyFilters"
                  placeholder="Enter visit ID"
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

          <!-- DataTable -->
          <DataTable
            :data="visitsStore.observations"
            :columns="columns"
            :loading="visitsStore.observationsLoading"
            :error="visitsStore.observationsError"
            empty-message="No observations found"
            @edit="handleEdit"
            @delete="handleDelete"
          >
            <template #cell-visit_info="{ item }">
              <router-link
                v-if="item.visit"
                :to="`/visits/visits/${item.visit}`"
                class="text-blue-600 hover:text-blue-800 font-medium"
              >
                Visit #{{ item.visit }}
              </router-link>
              <span v-else class="text-gray-400">N/A</span>
            </template>

            <template #cell-coefficient_name="{ item }">
              <span class="font-medium text-gray-700">{{ item.coefficient_name || 'N/A' }}</span>
            </template>

            <template #cell-product_name="{ item }">
              <router-link
                v-if="item.product"
                :to="`/catalog/products/${item.product}`"
                class="text-blue-600 hover:text-blue-800"
              >
                {{ item.product_name }}
              </router-link>
              <span v-else class="text-gray-400 text-sm italic">No product</span>
            </template>

            <template #cell-value="{ item }">
              <span class="font-semibold text-gray-900">{{ formatValue(item) }}</span>
            </template>

            <template #cell-timestamp="{ item }">
              <span class="text-gray-600 text-sm">{{ formatTimestamp(item.timestamp) }}</span>
            </template>

            <template #cell-location="{ item }">
              <span v-if="item.latitude && item.longitude" class="text-gray-600 text-xs">
                {{ item.latitude.toFixed(4) }}, {{ item.longitude.toFixed(4) }}
              </span>
              <span v-else class="text-gray-400 text-sm italic">No location</span>
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
import { useVisitsStore } from '@/stores/visits'
import Navbar from '@/components/layout/Navbar.vue'
import Sidebar from '@/components/layout/Sidebar.vue'
import DataTable from '@/components/common/DataTable.vue'

const router = useRouter()
const visitsStore = useVisitsStore()

const columns = ref([
  { key: 'visit_info', label: 'Visit' },
  { key: 'coefficient_name', label: 'Coefficient' },
  { key: 'product_name', label: 'Product' },
  { key: 'value', label: 'Value' },
  { key: 'timestamp', label: 'Recorded' },
  { key: 'location', label: 'Location' }
])

const filters = ref({
  visit: '',
  date_from: '',
  date_to: ''
})

const formatValue = (observation) => {
  if (observation.value_text) return observation.value_text
  if (observation.value_number !== null) return observation.value_number
  if (observation.value_boolean !== null) return observation.value_boolean ? 'Yes' : 'No'
  if (observation.value_date) return new Date(observation.value_date).toLocaleDateString()
  return 'N/A'
}

const formatTimestamp = (timestamp) => {
  if (!timestamp) return 'N/A'
  return new Date(timestamp).toLocaleString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const handleEdit = (observation) => {
  router.push(`/visits/observations/${observation.id}/edit`)
}

const handleDelete = async (observation) => {
  if (confirm(`Delete observation for "${observation.coefficient_name}"? This action cannot be undone.`)) {
    try {
      await visitsStore.deleteObservation(observation.id)
      alert('Observation deleted successfully')
    } catch (error) {
      alert('Failed to delete observation: ' + (error.response?.data?.detail || error.message))
    }
  }
}

const applyFilters = async () => {
  const params = {}
  if (filters.value.visit) params.visit = filters.value.visit
  if (filters.value.date_from) params.timestamp_after = filters.value.date_from
  if (filters.value.date_to) params.timestamp_before = filters.value.date_to

  await visitsStore.fetchObservations(params)
}

onMounted(async () => {
  await visitsStore.fetchObservations()
})
</script>
