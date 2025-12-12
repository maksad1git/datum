<template>
  <div class="min-h-screen bg-gray-50">
    <Navbar />

    <div class="flex">
      <Sidebar />

      <main class="flex-1 p-8 ml-64">
        <div class="max-w-7xl mx-auto">
          <!-- Header -->
          <div class="flex justify-between items-center mb-6">
            <h1 class="text-3xl font-bold text-gray-900">Brands</h1>
            <button
              @click="handleCreate"
              class="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-lg shadow-md transition duration-200"
            >
              + Create Brand
            </button>
          </div>

          <!-- DataTable -->
          <DataTable
            :data="catalogStore.brands"
            :columns="columns"
            :loading="catalogStore.brandsLoading"
            :error="catalogStore.brandsError"
            empty-message="No brands found"
            @edit="handleEdit"
            @delete="handleDelete"
          >
            <template #cell-name="{ item }">
              <router-link
                :to="`/catalog/brands/${item.id}`"
                class="text-blue-600 hover:text-blue-800 font-medium"
              >
                {{ item.name }}
              </router-link>
            </template>

            <template #cell-code="{ item }">
              <code class="bg-gray-100 px-2 py-1 rounded text-sm">{{ item.code }}</code>
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

            <template #cell-logo="{ item }">
              <img
                v-if="item.logo"
                :src="item.logo"
                :alt="item.name"
                class="h-8 w-8 rounded object-cover"
              />
              <span v-else class="text-gray-400 text-sm">No logo</span>
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
  { key: 'logo', label: 'Logo' },
  { key: 'name', label: 'Name' },
  { key: 'code', label: 'Code' },
  { key: 'description', label: 'Description' },
  { key: 'is_active', label: 'Status' }
])

const handleCreate = () => {
  router.push('/catalog/brands/create')
}

const handleEdit = (brand) => {
  router.push(`/catalog/brands/${brand.id}/edit`)
}

const handleDelete = async (brand) => {
  if (confirm(`Delete brand "${brand.name}"? This action cannot be undone.`)) {
    try {
      await catalogStore.deleteBrand(brand.id)
      alert('Brand deleted successfully')
    } catch (error) {
      alert('Failed to delete brand: ' + (error.response?.data?.detail || error.message))
    }
  }
}

onMounted(async () => {
  await catalogStore.fetchBrands()
})
</script>
