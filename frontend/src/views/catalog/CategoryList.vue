<template>
  <div class="min-h-screen bg-gray-50">
    <Navbar />

    <div class="flex">
      <Sidebar />

      <main class="flex-1 p-8 ml-64">
        <div class="max-w-7xl mx-auto">
          <!-- Header -->
          <div class="flex justify-between items-center mb-6">
            <h1 class="text-3xl font-bold text-gray-900">Product Categories</h1>
            <button
              @click="handleCreate"
              class="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-lg shadow-md transition duration-200"
            >
              + Create Category
            </button>
          </div>

          <!-- DataTable -->
          <DataTable
            :data="catalogStore.categories"
            :columns="columns"
            :loading="catalogStore.categoriesLoading"
            :error="catalogStore.categoriesError"
            empty-message="No categories found"
            @edit="handleEdit"
            @delete="handleDelete"
          >
            <template #cell-name="{ item }">
              <div class="flex items-center">
                <span v-if="item.parent" class="text-gray-400 mr-2">└─</span>
                <router-link
                  :to="`/catalog/categories/${item.id}`"
                  class="text-blue-600 hover:text-blue-800 font-medium"
                >
                  {{ item.name }}
                </router-link>
              </div>
            </template>

            <template #cell-code="{ item }">
              <code class="bg-gray-100 px-2 py-1 rounded text-sm">{{ item.code }}</code>
            </template>

            <template #cell-parent_name="{ item }">
              <span v-if="item.parent_name" class="text-gray-700">{{ item.parent_name }}</span>
              <span v-else class="text-gray-400 text-sm italic">Root Category</span>
            </template>

            <template #cell-product_count="{ item }">
              <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                {{ item.product_count || 0 }} products
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
import { useCatalogStore } from '@/stores/catalog'
import Navbar from '@/components/layout/Navbar.vue'
import Sidebar from '@/components/layout/Sidebar.vue'
import DataTable from '@/components/common/DataTable.vue'

const router = useRouter()
const catalogStore = useCatalogStore()

const columns = ref([
  { key: 'name', label: 'Name' },
  { key: 'code', label: 'Code' },
  { key: 'parent_name', label: 'Parent Category' },
  { key: 'product_count', label: 'Products' },
  { key: 'is_active', label: 'Status' }
])

const handleCreate = () => {
  router.push('/catalog/categories/create')
}

const handleEdit = (category) => {
  router.push(`/catalog/categories/${category.id}/edit`)
}

const handleDelete = async (category) => {
  if (confirm(`Delete category "${category.name}"? This action cannot be undone.`)) {
    try {
      await catalogStore.deleteCategory(category.id)
      alert('Category deleted successfully')
    } catch (error) {
      alert('Failed to delete category: ' + (error.response?.data?.detail || error.message))
    }
  }
}

onMounted(async () => {
  await catalogStore.fetchCategories()
})
</script>
