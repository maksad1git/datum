<template>
  <div class="min-h-screen bg-gray-50">
    <Navbar />

    <div class="flex">
      <Sidebar />

      <main class="flex-1 p-8 ml-64">
        <div class="max-w-7xl mx-auto">
          <!-- Header -->
          <div class="flex justify-between items-center mb-6">
            <h1 class="text-3xl font-bold text-gray-900">Countries</h1>
            <button class="btn btn-primary">
              + Create New
            </button>
          </div>

          <!-- DataTable -->
          <DataTable
            :data="geographyStore.countries"
            :columns="columns"
            :loading="geographyStore.loading"
            :error="geographyStore.error"
            empty-message="No countries found"
            @edit="handleEdit"
            @delete="handleDelete"
          >
            <template #cell-name="{ item }">
              <router-link
                :to="`/geo/countries/${item.id}`"
                class="text-primary hover:text-blue-700 font-medium"
              >
                {{ item.name }}
              </router-link>
            </template>

            <template #cell-code="{ item }">
              <code class="bg-gray-100 px-2 py-1 rounded text-sm">{{ item.code }}</code>
            </template>

            <template #cell-data_type="{ item }">
              <span
                class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full"
                :class="{
                  'bg-green-100 text-green-800': item.data_type === 'actual',
                  'bg-blue-100 text-blue-800': item.data_type === 'monitoring',
                  'bg-purple-100 text-purple-800': item.data_type === 'expert',
                  'bg-gray-100 text-gray-800': !item.data_type
                }"
              >
                {{ item.data_type || 'N/A' }}
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
import { useGeographyStore } from '@/stores/geography'
import Navbar from '@/components/layout/Navbar.vue'
import Sidebar from '@/components/layout/Sidebar.vue'
import DataTable from '@/components/common/DataTable.vue'

const router = useRouter()
const geographyStore = useGeographyStore()

const columns = ref([
  { key: 'name', label: 'Name' },
  { key: 'code', label: 'Code' },
  { key: 'global_market_name', label: 'Global Market' },
  { key: 'data_type', label: 'Data Type' }
])

const handleEdit = (country) => {
  router.push(`/geo/countries/${country.id}/edit`)
}

const handleDelete = async (country) => {
  if (confirm(`Delete country "${country.name}"?`)) {
    const result = await geographyStore.deleteCountry(country.id)
    if (result.success) {
      alert('Country deleted successfully')
    } else {
      alert('Failed to delete country: ' + result.error)
    }
  }
}

onMounted(async () => {
  await geographyStore.fetchCountries()
})
</script>
