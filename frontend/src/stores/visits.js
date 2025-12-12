import { defineStore } from 'pinia'
import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'
const API_VERSION = import.meta.env.VITE_API_VERSION || 'v1'

export const useVisitsStore = defineStore('visits', {
  state: () => ({
    // Visit Types
    visitTypes: [],
    currentVisitType: null,

    // Visits
    visits: [],
    currentVisit: null,

    // Observations
    observations: [],
    currentObservation: null,

    // Visit Media
    visitMedia: [],
    currentVisitMedia: null,

    // Sales
    sales: [],
    currentSale: null,

    // Loading states
    visitTypesLoading: false,
    visitsLoading: false,
    observationsLoading: false,
    visitMediaLoading: false,
    salesLoading: false,

    // Error states
    visitTypesError: null,
    visitsError: null,
    observationsError: null,
    visitMediaError: null,
    salesError: null,
  }),

  getters: {
    // Visit Type getters
    activeVisitTypes: (state) => state.visitTypes.filter(vt => vt.is_active),
    visitTypeById: (state) => (id) => state.visitTypes.find(vt => vt.id === id),

    // Visit getters
    visitById: (state) => (id) => state.visits.find(v => v.id === id),
    visitsByStatus: (state) => (status) => state.visits.filter(v => v.status === status),
    visitsByOutlet: (state) => (outletId) => state.visits.filter(v => v.outlet === outletId),
    visitsByUser: (state) => (userId) => state.visits.filter(v => v.user === userId),
    plannedVisits: (state) => state.visits.filter(v => v.status === 'planned'),
    completedVisits: (state) => state.visits.filter(v => v.status === 'completed'),

    // Observation getters
    observationById: (state) => (id) => state.observations.find(o => o.id === id),
    observationsByVisit: (state) => (visitId) => state.observations.filter(o => o.visit === visitId),

    // Visit Media getters
    visitMediaById: (state) => (id) => state.visitMedia.find(vm => vm.id === id),
    visitMediaByVisit: (state) => (visitId) => state.visitMedia.filter(vm => vm.visit === visitId),

    // Sale getters
    saleById: (state) => (id) => state.sales.find(s => s.id === id),
    salesByVisit: (state) => (visitId) => state.sales.filter(s => s.visit === visitId),
    salesByOutlet: (state) => (outletId) => state.sales.filter(s => s.outlet === outletId),
  },

  actions: {
    // ==================== VISIT TYPES ====================
    async fetchVisitTypes(params = {}) {
      this.visitTypesLoading = true
      this.visitTypesError = null
      try {
        const response = await axios.get(`${API_BASE}/api/${API_VERSION}/visits/visit-types/`, { params })
        this.visitTypes = response.data.results || response.data
        return this.visitTypes
      } catch (error) {
        this.visitTypesError = error.response?.data?.detail || error.message
        throw error
      } finally {
        this.visitTypesLoading = false
      }
    },

    async fetchVisitType(id) {
      this.visitTypesLoading = true
      this.visitTypesError = null
      try {
        const response = await axios.get(`${API_BASE}/api/${API_VERSION}/visits/visit-types/${id}/`)
        this.currentVisitType = response.data
        return this.currentVisitType
      } catch (error) {
        this.visitTypesError = error.response?.data?.detail || error.message
        throw error
      } finally {
        this.visitTypesLoading = false
      }
    },

    async createVisitType(visitTypeData) {
      this.visitTypesLoading = true
      this.visitTypesError = null
      try {
        const response = await axios.post(`${API_BASE}/api/${API_VERSION}/visits/visit-types/`, visitTypeData)
        this.visitTypes.push(response.data)
        return response.data
      } catch (error) {
        this.visitTypesError = error.response?.data || error.message
        throw error
      } finally {
        this.visitTypesLoading = false
      }
    },

    async updateVisitType(id, visitTypeData) {
      this.visitTypesLoading = true
      this.visitTypesError = null
      try {
        const response = await axios.put(`${API_BASE}/api/${API_VERSION}/visits/visit-types/${id}/`, visitTypeData)
        const index = this.visitTypes.findIndex(vt => vt.id === id)
        if (index !== -1) {
          this.visitTypes[index] = response.data
        }
        return response.data
      } catch (error) {
        this.visitTypesError = error.response?.data || error.message
        throw error
      } finally {
        this.visitTypesLoading = false
      }
    },

    async deleteVisitType(id) {
      this.visitTypesLoading = true
      this.visitTypesError = null
      try {
        await axios.delete(`${API_BASE}/api/${API_VERSION}/visits/visit-types/${id}/`)
        this.visitTypes = this.visitTypes.filter(vt => vt.id !== id)
      } catch (error) {
        this.visitTypesError = error.response?.data?.detail || error.message
        throw error
      } finally {
        this.visitTypesLoading = false
      }
    },

    // ==================== VISITS ====================
    async fetchVisits(params = {}) {
      this.visitsLoading = true
      this.visitsError = null
      try {
        const response = await axios.get(`${API_BASE}/api/${API_VERSION}/visits/visits/`, { params })
        this.visits = response.data.results || response.data
        return this.visits
      } catch (error) {
        this.visitsError = error.response?.data?.detail || error.message
        throw error
      } finally {
        this.visitsLoading = false
      }
    },

    async fetchVisit(id) {
      this.visitsLoading = true
      this.visitsError = null
      try {
        const response = await axios.get(`${API_BASE}/api/${API_VERSION}/visits/visits/${id}/`)
        this.currentVisit = response.data
        return this.currentVisit
      } catch (error) {
        this.visitsError = error.response?.data?.detail || error.message
        throw error
      } finally {
        this.visitsLoading = false
      }
    },

    async createVisit(visitData) {
      this.visitsLoading = true
      this.visitsError = null
      try {
        const response = await axios.post(`${API_BASE}/api/${API_VERSION}/visits/visits/`, visitData)
        this.visits.push(response.data)
        return response.data
      } catch (error) {
        this.visitsError = error.response?.data || error.message
        throw error
      } finally {
        this.visitsLoading = false
      }
    },

    async updateVisit(id, visitData) {
      this.visitsLoading = true
      this.visitsError = null
      try {
        const response = await axios.put(`${API_BASE}/api/${API_VERSION}/visits/visits/${id}/`, visitData)
        const index = this.visits.findIndex(v => v.id === id)
        if (index !== -1) {
          this.visits[index] = response.data
        }
        return response.data
      } catch (error) {
        this.visitsError = error.response?.data || error.message
        throw error
      } finally {
        this.visitsLoading = false
      }
    },

    async deleteVisit(id) {
      this.visitsLoading = true
      this.visitsError = null
      try {
        await axios.delete(`${API_BASE}/api/${API_VERSION}/visits/visits/${id}/`)
        this.visits = this.visits.filter(v => v.id !== id)
      } catch (error) {
        this.visitsError = error.response?.data?.detail || error.message
        throw error
      } finally {
        this.visitsLoading = false
      }
    },

    // ==================== OBSERVATIONS ====================
    async fetchObservations(params = {}) {
      this.observationsLoading = true
      this.observationsError = null
      try {
        const response = await axios.get(`${API_BASE}/api/${API_VERSION}/visits/observations/`, { params })
        this.observations = response.data.results || response.data
        return this.observations
      } catch (error) {
        this.observationsError = error.response?.data?.detail || error.message
        throw error
      } finally {
        this.observationsLoading = false
      }
    },

    async fetchObservation(id) {
      this.observationsLoading = true
      this.observationsError = null
      try {
        const response = await axios.get(`${API_BASE}/api/${API_VERSION}/visits/observations/${id}/`)
        this.currentObservation = response.data
        return this.currentObservation
      } catch (error) {
        this.observationsError = error.response?.data?.detail || error.message
        throw error
      } finally {
        this.observationsLoading = false
      }
    },

    async createObservation(observationData) {
      this.observationsLoading = true
      this.observationsError = null
      try {
        const response = await axios.post(`${API_BASE}/api/${API_VERSION}/visits/observations/`, observationData)
        this.observations.push(response.data)
        return response.data
      } catch (error) {
        this.observationsError = error.response?.data || error.message
        throw error
      } finally {
        this.observationsLoading = false
      }
    },

    async updateObservation(id, observationData) {
      this.observationsLoading = true
      this.observationsError = null
      try {
        const response = await axios.put(`${API_BASE}/api/${API_VERSION}/visits/observations/${id}/`, observationData)
        const index = this.observations.findIndex(o => o.id === id)
        if (index !== -1) {
          this.observations[index] = response.data
        }
        return response.data
      } catch (error) {
        this.observationsError = error.response?.data || error.message
        throw error
      } finally {
        this.observationsLoading = false
      }
    },

    async deleteObservation(id) {
      this.observationsLoading = true
      this.observationsError = null
      try {
        await axios.delete(`${API_BASE}/api/${API_VERSION}/visits/observations/${id}/`)
        this.observations = this.observations.filter(o => o.id !== id)
      } catch (error) {
        this.observationsError = error.response?.data?.detail || error.message
        throw error
      } finally {
        this.observationsLoading = false
      }
    },

    // ==================== VISIT MEDIA ====================
    async fetchVisitMedia(params = {}) {
      this.visitMediaLoading = true
      this.visitMediaError = null
      try {
        const response = await axios.get(`${API_BASE}/api/${API_VERSION}/visits/visit-media/`, { params })
        this.visitMedia = response.data.results || response.data
        return this.visitMedia
      } catch (error) {
        this.visitMediaError = error.response?.data?.detail || error.message
        throw error
      } finally {
        this.visitMediaLoading = false
      }
    },

    async fetchVisitMediaItem(id) {
      this.visitMediaLoading = true
      this.visitMediaError = null
      try {
        const response = await axios.get(`${API_BASE}/api/${API_VERSION}/visits/visit-media/${id}/`)
        this.currentVisitMedia = response.data
        return this.currentVisitMedia
      } catch (error) {
        this.visitMediaError = error.response?.data?.detail || error.message
        throw error
      } finally {
        this.visitMediaLoading = false
      }
    },

    async createVisitMedia(visitMediaData) {
      this.visitMediaLoading = true
      this.visitMediaError = null
      try {
        const response = await axios.post(`${API_BASE}/api/${API_VERSION}/visits/visit-media/`, visitMediaData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        })
        this.visitMedia.push(response.data)
        return response.data
      } catch (error) {
        this.visitMediaError = error.response?.data || error.message
        throw error
      } finally {
        this.visitMediaLoading = false
      }
    },

    async updateVisitMedia(id, visitMediaData) {
      this.visitMediaLoading = true
      this.visitMediaError = null
      try {
        const response = await axios.put(`${API_BASE}/api/${API_VERSION}/visits/visit-media/${id}/`, visitMediaData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        })
        const index = this.visitMedia.findIndex(vm => vm.id === id)
        if (index !== -1) {
          this.visitMedia[index] = response.data
        }
        return response.data
      } catch (error) {
        this.visitMediaError = error.response?.data || error.message
        throw error
      } finally {
        this.visitMediaLoading = false
      }
    },

    async deleteVisitMedia(id) {
      this.visitMediaLoading = true
      this.visitMediaError = null
      try {
        await axios.delete(`${API_BASE}/api/${API_VERSION}/visits/visit-media/${id}/`)
        this.visitMedia = this.visitMedia.filter(vm => vm.id !== id)
      } catch (error) {
        this.visitMediaError = error.response?.data?.detail || error.message
        throw error
      } finally {
        this.visitMediaLoading = false
      }
    },

    // ==================== SALES ====================
    async fetchSales(params = {}) {
      this.salesLoading = true
      this.salesError = null
      try {
        const response = await axios.get(`${API_BASE}/api/${API_VERSION}/visits/sales/`, { params })
        this.sales = response.data.results || response.data
        return this.sales
      } catch (error) {
        this.salesError = error.response?.data?.detail || error.message
        throw error
      } finally {
        this.salesLoading = false
      }
    },

    async fetchSale(id) {
      this.salesLoading = true
      this.salesError = null
      try {
        const response = await axios.get(`${API_BASE}/api/${API_VERSION}/visits/sales/${id}/`)
        this.currentSale = response.data
        return this.currentSale
      } catch (error) {
        this.salesError = error.response?.data?.detail || error.message
        throw error
      } finally {
        this.salesLoading = false
      }
    },

    async createSale(saleData) {
      this.salesLoading = true
      this.salesError = null
      try {
        const response = await axios.post(`${API_BASE}/api/${API_VERSION}/visits/sales/`, saleData)
        this.sales.push(response.data)
        return response.data
      } catch (error) {
        this.salesError = error.response?.data || error.message
        throw error
      } finally {
        this.salesLoading = false
      }
    },

    async updateSale(id, saleData) {
      this.salesLoading = true
      this.salesError = null
      try {
        const response = await axios.put(`${API_BASE}/api/${API_VERSION}/visits/sales/${id}/`, saleData)
        const index = this.sales.findIndex(s => s.id === id)
        if (index !== -1) {
          this.sales[index] = response.data
        }
        return response.data
      } catch (error) {
        this.salesError = error.response?.data || error.message
        throw error
      } finally {
        this.salesLoading = false
      }
    },

    async deleteSale(id) {
      this.salesLoading = true
      this.salesError = null
      try {
        await axios.delete(`${API_BASE}/api/${API_VERSION}/visits/sales/${id}/`)
        this.sales = this.sales.filter(s => s.id !== id)
      } catch (error) {
        this.salesError = error.response?.data?.detail || error.message
        throw error
      } finally {
        this.salesLoading = false
      }
    },
  },
})
