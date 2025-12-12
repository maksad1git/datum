<template>
  <div class="min-h-screen bg-gray-50">
    <Navbar />

    <div class="flex">
      <Sidebar />

      <main class="flex-1 p-8 ml-64">
        <div class="max-w-7xl mx-auto">
          <!-- Header -->
          <div class="flex justify-between items-center mb-6">
            <h1 class="text-3xl font-bold text-gray-900">Visit Types</h1>
            <button
              @click="handleCreate"
              class="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-lg shadow-md transition duration-200"
            >
              + Create Visit Type
            </button>
          </div>

          <!-- DataTable -->
          <DataTable
            :data="visitsStore.visitTypes"
            :columns="columns"
            :loading="visitsStore.visitTypesLoading"
            :error="visitsStore.visitTypesError"
            empty-message="No visit types found"
            @edit="handleEdit"
            @delete="handleDelete"
          >
            <template #cell-name="{ item }">
              <router-link
                :to="`/visits/visit-types/${item.id}`"
                class="text-blue-600 hover:text-blue-800 font-medium"
              >
                {{ item.name }}
              </router-link>
            </template>

            <template #cell-code="{ item }">
              <code class="bg-gray-100 px-2 py-1 rounded text-sm">{{ item.code }}</code>
            </template>

            <template #cell-description="{ item }">
              <span class="text-gray-600 text-sm">{{ item.description || 'No description' }}</span>
            </template>

            <template #cell-form_template_name="{ item }">
              <span v-if="item.form_template_name" class="text-gray-700">
                {{ item.form_template_name }}
              </span>
              <span v-else class="text-gray-400 text-sm italic">No template</span>
            </template>

            <template #cell-coefficient_count="{ item }">
              <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-purple-100 text-purple-800">
                {{ item.coefficient_count || 0 }} coefficients
              </span>
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
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useVisitsStore } from '@/stores/visits'
import Navbar from '@/components/layout/Navbar.vue'
import Sidebar from '@/components/layout/Sidebar.vue'
import DataTable from '@/components/common/DataTable.vue'

const router = useRouter()
const visitsStore = useVisitsStore()

const columns = ref([
  { key: 'name', label: 'Name' },
  { key: 'code', label: 'Code' },
  { key: 'description', label: 'Description' },
  { key: 'form_template_name', label: 'Form Template' },
  { key: 'coefficient_count', label: 'Coefficients' },
  { key: 'is_active', label: 'Status' }
])

const handleCreate = () => {
  router.push('/visits/visit-types/create')
}

const handleEdit = (visitType) => {
  router.push(`/visits/visit-types/${visitType.id}/edit`)
}

const handleDelete = async (visitType) => {
  if (confirm(`Delete visit type "${visitType.name}"? This action cannot be undone.`)) {
    try {
      await visitsStore.deleteVisitType(visitType.id)
      alert('Visit type deleted successfully')
    } catch (error) {
      alert('Failed to delete visit type: ' + (error.response?.data?.detail || error.message))
    }
  }
}

onMounted(async () => {
  await visitsStore.fetchVisitTypes()
})
</script>
