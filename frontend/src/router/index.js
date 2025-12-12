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
    },

    // CATALOG Routes
    {
      path: '/catalog',
      meta: { requiresAuth: true },
      children: [
        {
          path: 'brands',
          name: 'brand-list',
          component: () => import('@/views/catalog/BrandList.vue')
        },
        {
          path: 'brands/create',
          name: 'brand-create',
          component: () => import('@/views/catalog/BrandForm.vue')
        },
        {
          path: 'brands/:id',
          name: 'brand-detail',
          component: () => import('@/views/catalog/BrandDetail.vue')
        },
        {
          path: 'brands/:id/edit',
          name: 'brand-edit',
          component: () => import('@/views/catalog/BrandForm.vue')
        },
        {
          path: 'categories',
          name: 'category-list',
          component: () => import('@/views/catalog/CategoryList.vue')
        },
        {
          path: 'products',
          name: 'product-list',
          component: () => import('@/views/catalog/ProductList.vue')
        },
        {
          path: 'products/create',
          name: 'product-create',
          component: () => import('@/views/catalog/ProductForm.vue')
        },
        {
          path: 'products/:id',
          name: 'product-detail',
          component: () => import('@/views/catalog/ProductDetail.vue')
        },
        {
          path: 'products/:id/edit',
          name: 'product-edit',
          component: () => import('@/views/catalog/ProductForm.vue')
        },
        {
          path: 'preinstalls',
          name: 'preinstall-list',
          component: () => import('@/views/catalog/PreinstallList.vue')
        }
      ]
    },

    // VISITS Routes
    {
      path: '/visits',
      meta: { requiresAuth: true },
      children: [
        {
          path: 'visit-types',
          name: 'visit-type-list',
          component: () => import('@/views/visits/VisitTypeList.vue')
        },
        {
          path: 'visits',
          name: 'visit-list',
          component: () => import('@/views/visits/VisitList.vue')
        },
        {
          path: 'visits/create',
          name: 'visit-create',
          component: () => import('@/views/visits/VisitForm.vue')
        },
        {
          path: 'visits/:id',
          name: 'visit-detail',
          component: () => import('@/views/visits/VisitDetail.vue')
        },
        {
          path: 'visits/:id/edit',
          name: 'visit-edit',
          component: () => import('@/views/visits/VisitForm.vue')
        },
        {
          path: 'observations',
          name: 'observation-list',
          component: () => import('@/views/visits/ObservationList.vue')
        },
        {
          path: 'sales',
          name: 'sale-list',
          component: () => import('@/views/visits/SaleList.vue')
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
