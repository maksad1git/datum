import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/auth/Login.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: '/',
      name: 'home',
      component: () => import('@/views/Home.vue'),
      meta: { requiresAuth: true }
    },

    // GEO Routes
    {
      path: '/geo',
      meta: { requiresAuth: true },
      children: [
        {
          path: 'countries',
          name: 'country-list',
          component: () => import('@/views/geo/CountryList.vue')
        },
        {
          path: 'countries/:id',
          name: 'country-detail',
          component: () => import('@/views/geo/CountryDetail.vue')
        },
        {
          path: 'regions',
          name: 'region-list',
          component: () => import('@/views/geo/RegionList.vue')
        },
        {
          path: 'cities',
          name: 'city-list',
          component: () => import('@/views/geo/CityList.vue')
        },
        {
          path: 'districts',
          name: 'district-list',
          component: () => import('@/views/geo/DistrictList.vue')
        },
        {
          path: 'channels',
          name: 'channel-list',
          component: () => import('@/views/geo/ChannelList.vue')
        },
        {
          path: 'outlets',
          name: 'outlet-list',
          component: () => import('@/views/geo/OutletList.vue')
        }
      ]
    }
  ]
})

// Navigation guard
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'login', query: { redirect: to.fullPath } })
  } else if (to.name === 'login' && authStore.isAuthenticated) {
    next({ name: 'home' })
  } else {
    next()
  }
})

export default router
