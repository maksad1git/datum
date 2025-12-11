import { defineStore } from 'pinia'
import axios from 'axios'

const API_BASE = 'http://127.0.0.1:8000/api/v1/geo'

export const useGeographyStore = defineStore('geography', {
  state: () => ({
    globalMarkets: [],
    countries: [],
    regions: [],
    cities: [],
    districts: [],
    channels: [],
    outlets: [],

    loading: false,
    error: null,
  }),

  getters: {
    getCountriesByGlobalMarket: (state) => (globalMarketId) => {
      return state.countries.filter(c => c.global_market === globalMarketId)
    },

    getRegionsByCountry: (state) => (countryId) => {
      return state.regions.filter(r => r.country === countryId)
    },

    getCitiesByRegion: (state) => (regionId) => {
      return state.cities.filter(c => c.region === regionId)
    },

    getDistrictsByCity: (state) => (cityId) => {
      return state.districts.filter(d => d.city === cityId)
    },

    getChannelsByDistrict: (state) => (districtId) => {
      return state.channels.filter(c => c.district === districtId)
    },

    getOutletsByChannel: (state) => (channelId) => {
      return state.outlets.filter(o => o.channel === channelId)
    }
  },

  actions: {
    async fetchGlobalMarkets() {
      this.loading = true
      try {
        const response = await axios.get(`${API_BASE}/globalmarkets/`)
        this.globalMarkets = response.data.results || response.data
        this.error = null
      } catch (error) {
        this.error = error.message
        console.error('Failed to fetch global markets:', error)
      } finally {
        this.loading = false
      }
    },

    async fetchCountries(filters = {}) {
      this.loading = true
      try {
        const response = await axios.get(`${API_BASE}/countries/`, { params: filters })
        this.countries = response.data.results || response.data
        this.error = null
      } catch (error) {
        this.error = error.message
        console.error('Failed to fetch countries:', error)
      } finally {
        this.loading = false
      }
    },

    async fetchRegions(filters = {}) {
      this.loading = true
      try {
        const response = await axios.get(`${API_BASE}/regions/`, { params: filters })
        this.regions = response.data.results || response.data
        this.error = null
      } catch (error) {
        this.error = error.message
        console.error('Failed to fetch regions:', error)
      } finally {
        this.loading = false
      }
    },

    async fetchCities(filters = {}) {
      this.loading = true
      try {
        const response = await axios.get(`${API_BASE}/cities/`, { params: filters })
        this.cities = response.data.results || response.data
        this.error = null
      } catch (error) {
        this.error = error.message
        console.error('Failed to fetch cities:', error)
      } finally {
        this.loading = false
      }
    },

    async fetchDistricts(filters = {}) {
      this.loading = true
      try {
        const response = await axios.get(`${API_BASE}/districts/`, { params: filters })
        this.districts = response.data.results || response.data
        this.error = null
      } catch (error) {
        this.error = error.message
        console.error('Failed to fetch districts:', error)
      } finally {
        this.loading = false
      }
    },

    async fetchChannels(filters = {}) {
      this.loading = true
      try {
        const response = await axios.get(`${API_BASE}/channels/`, { params: filters })
        this.channels = response.data.results || response.data
        this.error = null
      } catch (error) {
        this.error = error.message
        console.error('Failed to fetch channels:', error)
      } finally {
        this.loading = false
      }
    },

    async fetchOutlets(filters = {}) {
      this.loading = true
      try {
        const response = await axios.get(`${API_BASE}/outlets/`, { params: filters })
        this.outlets = response.data.results || response.data
        this.error = null
      } catch (error) {
        this.error = error.message
        console.error('Failed to fetch outlets:', error)
      } finally {
        this.loading = false
      }
    },

    async createCountry(data) {
      try {
        const response = await axios.post(`${API_BASE}/countries/`, data)
        this.countries.push(response.data)
        return { success: true, data: response.data }
      } catch (error) {
        return { success: false, error: error.response?.data || error.message }
      }
    },

    async updateCountry(id, data) {
      try {
        const response = await axios.patch(`${API_BASE}/countries/${id}/`, data)
        const index = this.countries.findIndex(c => c.id === id)
        if (index !== -1) {
          this.countries[index] = response.data
        }
        return { success: true, data: response.data }
      } catch (error) {
        return { success: false, error: error.response?.data || error.message }
      }
    },

    async deleteCountry(id) {
      try {
        await axios.delete(`${API_BASE}/countries/${id}/`)
        this.countries = this.countries.filter(c => c.id !== id)
        return { success: true }
      } catch (error) {
        return { success: false, error: error.response?.data || error.message }
      }
    }
  }
})
