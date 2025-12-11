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

          <!-- Loading state -->
          <div v-if="geographyStore.loading" class="text-center py-12">
            <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
            <p class="mt-4 text-gray-600">Loading countries...</p>
          </div>

          <!-- Error state -->
          <div v-else-if="geographyStore.error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
            Error: {{ geographyStore.error }}
          </div>

          <!-- Countries table -->
          <div v-else class="bg-white rounded-lg shadow overflow-hidden">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Name
                  </th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Code
                  </th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Global Market
                  </th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Data Type
                  </th>
                  <th scope="col" class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="country in geographyStore.countries" :key="country.id" class="hover:bg-gray-50">
                  <td class="px-6 py-4 whitespace-nowrap">
                    <router-link
                      :to="`/geo/countries/${country.id}`"
                      class="text-primary hover:text-blue-700 font-medium"
                    >
                      {{ country.name }}
                    </router-link>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    <code class="bg-gray-100 px-2 py-1 rounded">{{ country.code }}</code>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {{ country.global_market_name || '-' }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full"
                          :class="{
                            'bg-green-100 text-green-800': country.data_type === 'actual',
                            'bg-blue-100 text-blue-800': country.data_type === 'monitoring',
                            'bg-purple-100 text-purple-800': country.data_type === 'expert',
                            'bg-gray-100 text-gray-800': !country.data_type
                          }">
                      {{ country.data_type || 'N/A' }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <button class="text-primary hover:text-blue-700 mr-3">
                      Edit
                    </button>
                    <button class="text-danger hover:text-red-700">
                      Delete
                    </button>
                  </td>
                </tr>

                <tr v-if="!geographyStore.countries.length">
                  <td colspan="5" class="px-6 py-12 text-center text-gray-500">
                    No countries found
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useGeographyStore } from '@/stores/geography'
import Navbar from '@/components/layout/Navbar.vue'
import Sidebar from '@/components/layout/Sidebar.vue'

const geographyStore = useGeographyStore()

onMounted(async () => {
  await geographyStore.fetchCountries()
})
</script>
