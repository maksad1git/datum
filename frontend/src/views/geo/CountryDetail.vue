<template>
  <div class="min-h-screen bg-gray-50">
    <Navbar />
    <div class="flex">
      <Sidebar />
      <main class="flex-1 p-8 ml-64">
        <div class="max-w-7xl mx-auto">
          <h1 class="text-3xl font-bold text-gray-900 mb-6">Country Detail</h1>
          <div class="bg-white rounded-lg shadow p-6">
            <p>Country ID: {{ $route.params.id }}</p>
            <p class="text-gray-500 mt-2">Detail view coming soon...</p>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import Navbar from '@/components/layout/Navbar.vue'
import Sidebar from '@/components/layout/Sidebar.vue'
</script>
