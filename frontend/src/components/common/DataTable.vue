<template>
  <div>
    <!-- Search and Actions -->
    <div class="mb-4 flex justify-between items-center">
      <div class="w-64">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Search..."
          class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary"
          @input="handleSearch"
        />
      </div>
      <slot name="actions"></slot>
    </div>

    <!-- Loading state -->
    <div v-if="loading" class="text-center py-12">
      <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
      <p class="mt-4 text-gray-600">Loading...</p>
    </div>

    <!-- Error state -->
    <div v-else-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
      Error: {{ error }}
    </div>

    <!-- Table -->
    <div v-else class="bg-white rounded-lg shadow overflow-hidden">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th
              v-for="column in columns"
              :key="column.key"
              scope="col"
              class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
            >
              {{ column.label }}
            </th>
            <th
              v-if="showActions"
              scope="col"
              class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider"
            >
              Actions
            </th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="item in data" :key="item.id" class="hover:bg-gray-50">
            <td
              v-for="column in columns"
              :key="column.key"
              class="px-6 py-4 whitespace-nowrap"
            >
              <slot :name="`cell-${column.key}`" :item="item">
                {{ getCellValue(item, column.key) }}
              </slot>
            </td>
            <td v-if="showActions" class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
              <slot name="actions" :item="item">
                <button
                  @click="$emit('edit', item)"
                  class="text-primary hover:text-blue-700 mr-3"
                >
                  Edit
                </button>
                <button
                  @click="$emit('delete', item)"
                  class="text-danger hover:text-red-700"
                >
                  Delete
                </button>
              </slot>
            </td>
          </tr>

          <tr v-if="!data.length">
            <td :colspan="columns.length + (showActions ? 1 : 0)" class="px-6 py-12 text-center text-gray-500">
              {{ emptyMessage }}
            </td>
          </tr>
        </tbody>
      </table>

      <!-- Pagination -->
      <div v-if="showPagination && totalPages > 1" class="bg-gray-50 px-4 py-3 flex items-center justify-between border-t border-gray-200">
        <div class="flex-1 flex justify-between sm:hidden">
          <button
            @click="$emit('page-change', currentPage - 1)"
            :disabled="currentPage === 1"
            class="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50"
          >
            Previous
          </button>
          <button
            @click="$emit('page-change', currentPage + 1)"
            :disabled="currentPage === totalPages"
            class="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50"
          >
            Next
          </button>
        </div>
        <div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
          <div>
            <p class="text-sm text-gray-700">
              Showing page <span class="font-medium">{{ currentPage }}</span> of <span class="font-medium">{{ totalPages }}</span>
            </p>
          </div>
          <div>
            <nav class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px">
              <button
                v-for="page in displayedPages"
                :key="page"
                @click="$emit('page-change', page)"
                :class="[
                  'relative inline-flex items-center px-4 py-2 border text-sm font-medium',
                  page === currentPage
                    ? 'z-10 bg-primary border-primary text-white'
                    : 'bg-white border-gray-300 text-gray-500 hover:bg-gray-50'
                ]"
              >
                {{ page }}
              </button>
            </nav>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  data: {
    type: Array,
    required: true
  },
  columns: {
    type: Array,
    required: true
  },
  loading: {
    type: Boolean,
    default: false
  },
  error: {
    type: String,
    default: null
  },
  showActions: {
    type: Boolean,
    default: true
  },
  showPagination: {
    type: Boolean,
    default: true
  },
  currentPage: {
    type: Number,
    default: 1
  },
  totalPages: {
    type: Number,
    default: 1
  },
  emptyMessage: {
    type: String,
    default: 'No data found'
  }
})

defineEmits(['edit', 'delete', 'page-change', 'search'])

const searchQuery = ref('')

const getCellValue = (item, key) => {
  return key.split('.').reduce((obj, k) => obj?.[k], item) || '-'
}

const handleSearch = () => {
  // Debounce implemented by parent
  props.$emit('search', searchQuery.value)
}

const displayedPages = computed(() => {
  const pages = []
  const maxVisible = 5
  let start = Math.max(1, props.currentPage - Math.floor(maxVisible / 2))
  let end = Math.min(props.totalPages, start + maxVisible - 1)

  if (end - start < maxVisible - 1) {
    start = Math.max(1, end - maxVisible + 1)
  }

  for (let i = start; i <= end; i++) {
    pages.push(i)
  }

  return pages
})
</script>
