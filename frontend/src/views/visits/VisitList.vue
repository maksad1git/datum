<template>
  <div class="min-h-screen bg-gray-50">
    <Navbar />

    <div class="flex">
      <Sidebar />

      <main class="flex-1 p-8 ml-64">
        <div class="max-w-7xl mx-auto">
          <!-- Header -->
          <div class="flex justify-between items-center mb-6">
            <h1 class="text-3xl font-bold text-gray-900">Mystery Shopping Visits</h1>
            <button
              @click="handleCreate"
              class="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-lg shadow-md transition duration-200"
            >
              + Create Visit
            </button>
          </div>

          <!-- Filters -->
          <div class="bg-white rounded-lg shadow-md p-4 mb-6">
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Visit Type</label>
                <select
                  v-model="filters.visit_type"
                  @change="applyFilters"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="">All Types</option>
                  <option v-for="type in visitsStore.visitTypes" :key="type.id" :value="type.id">
                    {{ type.name }}
                  </option>
                </select>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Status</label>
                <select
                  v-model="filters.status"
                  @change="applyFilters"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="">All Statuses</option>
                  <option value="planned">Planned</option>
                  <option value="in_progress">In Progress</option>
                  <option value="completed">Completed</option>
                  <option value="cancelled">Cancelled</option>
                </select>
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
            :data="visitsStore.visits"
            :columns="columns"
            :loading="visitsStore.visitsLoading"
            :error="visitsStore.visitsError"
            empty-message="No visits found"
            @edit="handleEdit"
            @delete="handleDelete"
          >
            <template #cell-visit_type_name="{ item }">
              <span class="font-medium text-gray-700">{{ item.visit_type_name || 'N/A' }}</span>
            </template>

            <template #cell-outlet_name="{ item }">
              <router-link
                :to="`/geo/outlets/${item.outlet}`"
                class="text-blue-600 hover:text-blue-800 font-medium"
              >
                {{ item.outlet_name || 'N/A' }}
              </router-link>
            </template>

            <template #cell-user_name="{ item }">
              <span class="text-gray-700">{{ item.user_name || 'N/A' }}</span>
            </template>

            <template #cell-planned_date="{ item }">
              <span class="text-gray-700">{{ formatDate(item.planned_date) }}</span>
            </template>

            <template #cell-status="{ item }">
              <span
                class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full"
                :class="getStatusClass(item.status)"
              >
                {{ item.status_display || item.status }}
              </span>
            </template>

            <template #cell-observation_count="{ item }">
              <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                {{ item.observation_count || 0 }} observations
              </span>
            </template>

            <template #cell-actions="{ item }">
              <div class="flex space-x-2">
                <router-link
                  :to="`/visits/visits/${item.id}`"
                  class="text-blue-600 hover:text-blue-900"
                  title="View Details"
                >
                  <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                  </svg>
                </router-link>
              </div>
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
  { key: 'visit_type_name', label: 'Visit Type' },
  { key: 'outlet_name', label: 'Outlet' },
  { key: 'user_name', label: 'Mystery Shopper' },
  { key: 'planned_date', label: 'Planned Date' },
  { key: 'status', label: 'Status' },
  { key: 'observation_count', label: 'Data' },
  { key: 'actions', label: 'Actions' }
])

const filters = ref({
  visit_type: '',
  status: '',
  date_from: '',
  date_to: ''
})

const getStatusClass = (status) => {
  const classes = {
    planned: 'bg-blue-100 text-blue-800',
    in_progress: 'bg-yellow-100 text-yellow-800',
    completed: 'bg-green-100 text-green-800',
    cancelled: 'bg-red-100 text-red-800'
  }
  return classes[status] || 'bg-gray-100 text-gray-800'
}

const formatDate = (date) => {
  if (!date) return 'N/A'
  return new Date(date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

const handleCreate = () => {
  router.push('/visits/visits/create')
}

const handleEdit = (visit) => {
  router.push(`/visits/visits/${visit.id}/edit`)
}

const handleDelete = async (visit) => {
  if (confirm(`Delete visit for "${visit.outlet_name}" on ${formatDate(visit.planned_date)}? This action cannot be undone.`)) {
    try {
      await visitsStore.deleteVisit(visit.id)
      alert('Visit deleted successfully')
    } catch (error) {
      alert('Failed to delete visit: ' + (error.response?.data?.detail || error.message))
    }
  }
}

const applyFilters = async () => {
  const params = {}
  if (filters.value.visit_type) params.visit_type = filters.value.visit_type
  if (filters.value.status) params.status = filters.value.status
  if (filters.value.date_from) params.planned_date_after = filters.value.date_from
  if (filters.value.date_to) params.planned_date_before = filters.value.date_to

  await visitsStore.fetchVisits(params)
}

onMounted(async () => {
  await Promise.all([
    visitsStore.fetchVisits(),
    visitsStore.fetchVisitTypes()
  ])
})
</script>
