import { defineStore } from 'pinia'
import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'
const API_VERSION = import.meta.env.VITE_API_VERSION || 'v1'

export const useCatalogStore = defineStore('catalog', {
  state: () => ({
    // Brands
    brands: [],
    currentBrand: null,

    // Categories
    categories: [],
    currentCategory: null,

    // Products
    products: [],
    currentProduct: null,

    // Preinstalls
    preinstalls: [],
    currentPreinstall: null,

    // Loading states
    brandsLoading: false,
    categoriesLoading: false,
    productsLoading: false,
    preinstallsLoading: false,

    // Error states
    brandsError: null,
    categoriesError: null,
    productsError: null,
    preinstallsError: null,
  }),

  getters: {
    // Brand getters
    activeBrands: (state) => state.brands.filter(b => b.is_active),
    brandById: (state) => (id) => state.brands.find(b => b.id === id),

    // Category getters
    activeCategories: (state) => state.categories.filter(c => c.is_active),
    categoryById: (state) => (id) => state.categories.find(c => c.id === id),
    rootCategories: (state) => state.categories.filter(c => !c.parent),

    // Product getters
    activeProducts: (state) => state.products.filter(p => p.is_active),
    productById: (state) => (id) => state.products.find(p => p.id === id),
    productsByBrand: (state) => (brandId) => state.products.filter(p => p.brand === brandId),
    productsByCategory: (state) => (categoryId) => state.products.filter(p => p.category === categoryId),

    // Preinstall getters
    activePreinstalls: (state) => state.preinstalls.filter(p => p.is_active),
    preinstallById: (state) => (id) => state.preinstalls.find(p => p.id === id),
  },

  actions: {
    // ==================== BRANDS ====================
    async fetchBrands(params = {}) {
      this.brandsLoading = true
      this.brandsError = null
      try {
        const response = await axios.get(`${API_BASE}/api/${API_VERSION}/catalog/brands/`, { params })
        this.brands = response.data.results || response.data
        return this.brands
      } catch (error) {
        this.brandsError = error.response?.data?.detail || error.message
        throw error
      } finally {
        this.brandsLoading = false
      }
    },

    async fetchBrand(id) {
      this.brandsLoading = true
      this.brandsError = null
      try {
        const response = await axios.get(`${API_BASE}/api/${API_VERSION}/catalog/brands/${id}/`)
        this.currentBrand = response.data
        return this.currentBrand
      } catch (error) {
        this.brandsError = error.response?.data?.detail || error.message
        throw error
      } finally {
        this.brandsLoading = false
      }
    },

    async createBrand(brandData) {
      this.brandsLoading = true
      this.brandsError = null
      try {
        const response = await axios.post(`${API_BASE}/api/${API_VERSION}/catalog/brands/`, brandData)
        this.brands.push(response.data)
        return response.data
      } catch (error) {
        this.brandsError = error.response?.data || error.message
        throw error
      } finally {
        this.brandsLoading = false
      }
    },

    async updateBrand(id, brandData) {
      this.brandsLoading = true
      this.brandsError = null
      try {
        const response = await axios.put(`${API_BASE}/api/${API_VERSION}/catalog/brands/${id}/`, brandData)
        const index = this.brands.findIndex(b => b.id === id)
        if (index !== -1) {
          this.brands[index] = response.data
        }
        return response.data
      } catch (error) {
        this.brandsError = error.response?.data || error.message
        throw error
      } finally {
        this.brandsLoading = false
      }
    },

    async deleteBrand(id) {
      this.brandsLoading = true
      this.brandsError = null
      try {
        await axios.delete(`${API_BASE}/api/${API_VERSION}/catalog/brands/${id}/`)
        this.brands = this.brands.filter(b => b.id !== id)
      } catch (error) {
        this.brandsError = error.response?.data?.detail || error.message
        throw error
      } finally {
        this.brandsLoading = false
      }
    },

    // ==================== CATEGORIES ====================
    async fetchCategories(params = {}) {
      this.categoriesLoading = true
      this.categoriesError = null
      try {
        const response = await axios.get(`${API_BASE}/api/${API_VERSION}/catalog/categories/`, { params })
        this.categories = response.data.results || response.data
        return this.categories
      } catch (error) {
        this.categoriesError = error.response?.data?.detail || error.message
        throw error
      } finally {
        this.categoriesLoading = false
      }
    },

    async fetchCategory(id) {
      this.categoriesLoading = true
      this.categoriesError = null
      try {
        const response = await axios.get(`${API_BASE}/api/${API_VERSION}/catalog/categories/${id}/`)
        this.currentCategory = response.data
        return this.currentCategory
      } catch (error) {
        this.categoriesError = error.response?.data?.detail || error.message
        throw error
      } finally {
        this.categoriesLoading = false
      }
    },

    async createCategory(categoryData) {
      this.categoriesLoading = true
      this.categoriesError = null
      try {
        const response = await axios.post(`${API_BASE}/api/${API_VERSION}/catalog/categories/`, categoryData)
        this.categories.push(response.data)
        return response.data
      } catch (error) {
        this.categoriesError = error.response?.data || error.message
        throw error
      } finally {
        this.categoriesLoading = false
      }
    },

    async updateCategory(id, categoryData) {
      this.categoriesLoading = true
      this.categoriesError = null
      try {
        const response = await axios.put(`${API_BASE}/api/${API_VERSION}/catalog/categories/${id}/`, categoryData)
        const index = this.categories.findIndex(c => c.id === id)
        if (index !== -1) {
          this.categories[index] = response.data
        }
        return response.data
      } catch (error) {
        this.categoriesError = error.response?.data || error.message
        throw error
      } finally {
        this.categoriesLoading = false
      }
    },

    async deleteCategory(id) {
      this.categoriesLoading = true
      this.categoriesError = null
      try {
        await axios.delete(`${API_BASE}/api/${API_VERSION}/catalog/categories/${id}/`)
        this.categories = this.categories.filter(c => c.id !== id)
      } catch (error) {
        this.categoriesError = error.response?.data?.detail || error.message
        throw error
      } finally {
        this.categoriesLoading = false
      }
    },

    // ==================== PRODUCTS ====================
    async fetchProducts(params = {}) {
      this.productsLoading = true
      this.productsError = null
      try {
        const response = await axios.get(`${API_BASE}/api/${API_VERSION}/catalog/products/`, { params })
        this.products = response.data.results || response.data
        return this.products
      } catch (error) {
        this.productsError = error.response?.data?.detail || error.message
        throw error
      } finally {
        this.productsLoading = false
      }
    },

    async fetchProduct(id) {
      this.productsLoading = true
      this.productsError = null
      try {
        const response = await axios.get(`${API_BASE}/api/${API_VERSION}/catalog/products/${id}/`)
        this.currentProduct = response.data
        return this.currentProduct
      } catch (error) {
        this.productsError = error.response?.data?.detail || error.message
        throw error
      } finally {
        this.productsLoading = false
      }
    },

    async createProduct(productData) {
      this.productsLoading = true
      this.productsError = null
      try {
        const response = await axios.post(`${API_BASE}/api/${API_VERSION}/catalog/products/`, productData)
        this.products.push(response.data)
        return response.data
      } catch (error) {
        this.productsError = error.response?.data || error.message
        throw error
      } finally {
        this.productsLoading = false
      }
    },

    async updateProduct(id, productData) {
      this.productsLoading = true
      this.productsError = null
      try {
        const response = await axios.put(`${API_BASE}/api/${API_VERSION}/catalog/products/${id}/`, productData)
        const index = this.products.findIndex(p => p.id === id)
        if (index !== -1) {
          this.products[index] = response.data
        }
        return response.data
      } catch (error) {
        this.productsError = error.response?.data || error.message
        throw error
      } finally {
        this.productsLoading = false
      }
    },

    async deleteProduct(id) {
      this.productsLoading = true
      this.productsError = null
      try {
        await axios.delete(`${API_BASE}/api/${API_VERSION}/catalog/products/${id}/`)
        this.products = this.products.filter(p => p.id !== id)
      } catch (error) {
        this.productsError = error.response?.data?.detail || error.message
        throw error
      } finally {
        this.productsLoading = false
      }
    },

    // ==================== PREINSTALLS ====================
    async fetchPreinstalls(params = {}) {
      this.preinstallsLoading = true
      this.preinstallsError = null
      try {
        const response = await axios.get(`${API_BASE}/api/${API_VERSION}/catalog/preinstalls/`, { params })
        this.preinstalls = response.data.results || response.data
        return this.preinstalls
      } catch (error) {
        this.preinstallsError = error.response?.data?.detail || error.message
        throw error
      } finally {
        this.preinstallsLoading = false
      }
    },

    async fetchPreinstall(id) {
      this.preinstallsLoading = true
      this.preinstallsError = null
      try {
        const response = await axios.get(`${API_BASE}/api/${API_VERSION}/catalog/preinstalls/${id}/`)
        this.currentPreinstall = response.data
        return this.currentPreinstall
      } catch (error) {
        this.preinstallsError = error.response?.data?.detail || error.message
        throw error
      } finally {
        this.preinstallsLoading = false
      }
    },

    async createPreinstall(preinstallData) {
      this.preinstallsLoading = true
      this.preinstallsError = null
      try {
        const response = await axios.post(`${API_BASE}/api/${API_VERSION}/catalog/preinstalls/`, preinstallData)
        this.preinstalls.push(response.data)
        return response.data
      } catch (error) {
        this.preinstallsError = error.response?.data || error.message
        throw error
      } finally {
        this.preinstallsLoading = false
      }
    },

    async updatePreinstall(id, preinstallData) {
      this.preinstallsLoading = true
      this.preinstallsError = null
      try {
        const response = await axios.put(`${API_BASE}/api/${API_VERSION}/catalog/preinstalls/${id}/`, preinstallData)
        const index = this.preinstalls.findIndex(p => p.id === id)
        if (index !== -1) {
          this.preinstalls[index] = response.data
        }
        return response.data
      } catch (error) {
        this.preinstallsError = error.response?.data || error.message
        throw error
      } finally {
        this.preinstallsLoading = false
      }
    },

    async deletePreinstall(id) {
      this.preinstallsLoading = true
      this.preinstallsError = null
      try {
        await axios.delete(`${API_BASE}/api/${API_VERSION}/catalog/preinstalls/${id}/`)
        this.preinstalls = this.preinstalls.filter(p => p.id !== id)
      } catch (error) {
        this.preinstallsError = error.response?.data?.detail || error.message
        throw error
      } finally {
        this.preinstallsLoading = false
      }
    },
  },
})
