import { defineStore } from 'pinia'
import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'
const API_VERSION = import.meta.env.VITE_API_VERSION || 'v1'

export const useAnalyticsStore = defineStore('analytics', {
  state: () => ({
    // Dashboards
    dashboards: [],
    currentDashboard: null,

    // Reports
    reports: [],
    currentReport: null,

    // Report Templates
    reportTemplates: [],
    currentReportTemplate: null,

    // Filter Presets
    filterPresets: [],
    currentFilterPreset: null,

    // Forecast Models
    forecastModels: [],
    currentForecastModel: null,

    // Loading states
    dashboardsLoading: false,
    reportsLoading: false,
    reportTemplatesLoading: false,
    filterPresetsLoading: false,
    forecastModelsLoading: false,

    // Error states
    dashboardsError: null,
    reportsError: null,
    reportTemplatesError: null,
    filterPresetsError: null,
    forecastModelsError: null,
  }),

  getters: {
    // Dashboard getters
    activeDashboards: (state) => state.dashboards.filter(d => d.is_active),
    publicDashboards: (state) => state.dashboards.filter(d => d.is_public),
    dashboardById: (state) => (id) => state.dashboards.find(d => d.id === id),
    dashboardsByType: (state) => (type) => state.dashboards.filter(d => d.dashboard_type === type),
    dashboardsByLevel: (state) => (level) => state.dashboards.filter(d => d.level === level),

    // Report getters
    reportById: (state) => (id) => state.reports.find(r => r.id === id),
    reportsByStatus: (state) => (status) => state.reports.filter(r => r.status === status),
    completedReports: (state) => state.reports.filter(r => r.status === 'completed'),
    pendingReports: (state) => state.reports.filter(r => r.status === 'pending'),

    // Report Template getters
    activeReportTemplates: (state) => state.reportTemplates.filter(rt => rt.is_active),
    reportTemplateById: (state) => (id) => state.reportTemplates.find(rt => rt.id === id),
    reportTemplatesByCategory: (state) => (category) => state.reportTemplates.filter(rt => rt.category === category),

    // Filter Preset getters
    publicFilterPresets: (state) => state.filterPresets.filter(fp => fp.is_public),
    filterPresetById: (state) => (id) => state.filterPresets.find(fp => fp.id === id),
    filterPresetsByType: (state) => (type) => state.filterPresets.filter(fp => fp.applies_to === type),

    // Forecast Model getters
    activeForecastModels: (state) => state.forecastModels.filter(fm => fm.status === 'active'),
    forecastModelById: (state) => (id) => state.forecastModels.find(fm => fm.id === id),
  },

  actions: {
    // ==================== DASHBOARDS ====================
    async fetchDashboards(params = {}) {
      this.dashboardsLoading = true
      this.dashboardsError = null
      try {
        const response = await axios.get(`${API_BASE}/api/${API_VERSION}/analytics/dashboards/`, { params })
        this.dashboards = response.data.results || response.data
        return this.dashboards
      } catch (error) {
        this.dashboardsError = error.response?.data?.detail || error.message
        throw error
      } finally {
        this.dashboardsLoading = false
      }
    },

    async fetchDashboard(id) {
      this.dashboardsLoading = true
      this.dashboardsError = null
      try {
        const response = await axios.get(`${API_BASE}/api/${API_VERSION}/analytics/dashboards/${id}/`)
        this.currentDashboard = response.data
        return this.currentDashboard
      } catch (error) {
        this.dashboardsError = error.response?.data?.detail || error.message
        throw error
      } finally {
        this.dashboardsLoading = false
      }
    },

    async createDashboard(dashboardData) {
      this.dashboardsLoading = true
      this.dashboardsError = null
      try {
        const response = await axios.post(`${API_BASE}/api/${API_VERSION}/analytics/dashboards/`, dashboardData)
        this.dashboards.push(response.data)
        return response.data
      } catch (error) {
        this.dashboardsError = error.response?.data || error.message
        throw error
      } finally {
        this.dashboardsLoading = false
      }
    },

    async updateDashboard(id, dashboardData) {
      this.dashboardsLoading = true
      this.dashboardsError = null
      try {
        const response = await axios.put(`${API_BASE}/api/${API_VERSION}/analytics/dashboards/${id}/`, dashboardData)
        const index = this.dashboards.findIndex(d => d.id === id)
        if (index !== -1) {
          this.dashboards[index] = response.data
        }
        return response.data
      } catch (error) {
        this.dashboardsError = error.response?.data || error.message
        throw error
      } finally {
        this.dashboardsLoading = false
      }
    },

    async deleteDashboard(id) {
      this.dashboardsLoading = true
      this.dashboardsError = null
      try {
        await axios.delete(`${API_BASE}/api/${API_VERSION}/analytics/dashboards/${id}/`)
        this.dashboards = this.dashboards.filter(d => d.id !== id)
      } catch (error) {
        this.dashboardsError = error.response?.data?.detail || error.message
        throw error
      } finally {
        this.dashboardsLoading = false
      }
    },

    // ==================== REPORTS ====================
    async fetchReports(params = {}) {
      this.reportsLoading = true
      this.reportsError = null
      try {
        const response = await axios.get(`${API_BASE}/api/${API_VERSION}/analytics/reports/`, { params })
        this.reports = response.data.results || response.data
        return this.reports
      } catch (error) {
        this.reportsError = error.response?.data?.detail || error.message
        throw error
      } finally {
        this.reportsLoading = false
      }
    },

    async fetchReport(id) {
      this.reportsLoading = true
      this.reportsError = null
      try {
        const response = await axios.get(`${API_BASE}/api/${API_VERSION}/analytics/reports/${id}/`)
        this.currentReport = response.data
        return this.currentReport
      } catch (error) {
        this.reportsError = error.response?.data?.detail || error.message
        throw error
      } finally {
        this.reportsLoading = false
      }
    },

    async createReport(reportData) {
      this.reportsLoading = true
      this.reportsError = null
      try {
        const response = await axios.post(`${API_BASE}/api/${API_VERSION}/analytics/reports/`, reportData)
        this.reports.push(response.data)
        return response.data
      } catch (error) {
        this.reportsError = error.response?.data || error.message
        throw error
      } finally {
        this.reportsLoading = false
      }
    },

    async updateReport(id, reportData) {
      this.reportsLoading = true
      this.reportsError = null
      try {
        const response = await axios.put(`${API_BASE}/api/${API_VERSION}/analytics/reports/${id}/`, reportData)
        const index = this.reports.findIndex(r => r.id === id)
        if (index !== -1) {
          this.reports[index] = response.data
        }
        return response.data
      } catch (error) {
        this.reportsError = error.response?.data || error.message
        throw error
      } finally {
        this.reportsLoading = false
      }
    },

    async deleteReport(id) {
      this.reportsLoading = true
      this.reportsError = null
      try {
        await axios.delete(`${API_BASE}/api/${API_VERSION}/analytics/reports/${id}/`)
        this.reports = this.reports.filter(r => r.id !== id)
      } catch (error) {
        this.reportsError = error.response?.data?.detail || error.message
        throw error
      } finally {
        this.reportsLoading = false
      }
    },

    // ==================== REPORT TEMPLATES ====================
    async fetchReportTemplates(params = {}) {
      this.reportTemplatesLoading = true
      this.reportTemplatesError = null
      try {
        const response = await axios.get(`${API_BASE}/api/${API_VERSION}/analytics/report-templates/`, { params })
        this.reportTemplates = response.data.results || response.data
        return this.reportTemplates
      } catch (error) {
        this.reportTemplatesError = error.response?.data?.detail || error.message
        throw error
      } finally {
        this.reportTemplatesLoading = false
      }
    },

    async fetchReportTemplate(id) {
      this.reportTemplatesLoading = true
      this.reportTemplatesError = null
      try {
        const response = await axios.get(`${API_BASE}/api/${API_VERSION}/analytics/report-templates/${id}/`)
        this.currentReportTemplate = response.data
        return this.currentReportTemplate
      } catch (error) {
        this.reportTemplatesError = error.response?.data?.detail || error.message
        throw error
      } finally {
        this.reportTemplatesLoading = false
      }
    },

    async createReportTemplate(templateData) {
      this.reportTemplatesLoading = true
      this.reportTemplatesError = null
      try {
        const response = await axios.post(`${API_BASE}/api/${API_VERSION}/analytics/report-templates/`, templateData)
        this.reportTemplates.push(response.data)
        return response.data
      } catch (error) {
        this.reportTemplatesError = error.response?.data || error.message
        throw error
      } finally {
        this.reportTemplatesLoading = false
      }
    },

    async updateReportTemplate(id, templateData) {
      this.reportTemplatesLoading = true
      this.reportTemplatesError = null
      try {
        const response = await axios.put(`${API_BASE}/api/${API_VERSION}/analytics/report-templates/${id}/`, templateData)
        const index = this.reportTemplates.findIndex(rt => rt.id === id)
        if (index !== -1) {
          this.reportTemplates[index] = response.data
        }
        return response.data
      } catch (error) {
        this.reportTemplatesError = error.response?.data || error.message
        throw error
      } finally {
        this.reportTemplatesLoading = false
      }
    },

    async deleteReportTemplate(id) {
      this.reportTemplatesLoading = true
      this.reportTemplatesError = null
      try {
        await axios.delete(`${API_BASE}/api/${API_VERSION}/analytics/report-templates/${id}/`)
        this.reportTemplates = this.reportTemplates.filter(rt => rt.id !== id)
      } catch (error) {
        this.reportTemplatesError = error.response?.data?.detail || error.message
        throw error
      } finally {
        this.reportTemplatesLoading = false
      }
    },

    // ==================== FILTER PRESETS ====================
    async fetchFilterPresets(params = {}) {
      this.filterPresetsLoading = true
      this.filterPresetsError = null
      try {
        const response = await axios.get(`${API_BASE}/api/${API_VERSION}/analytics/filter-presets/`, { params })
        this.filterPresets = response.data.results || response.data
        return this.filterPresets
      } catch (error) {
        this.filterPresetsError = error.response?.data?.detail || error.message
        throw error
      } finally {
        this.filterPresetsLoading = false
      }
    },

    async fetchFilterPreset(id) {
      this.filterPresetsLoading = true
      this.filterPresetsError = null
      try {
        const response = await axios.get(`${API_BASE}/api/${API_VERSION}/analytics/filter-presets/${id}/`)
        this.currentFilterPreset = response.data
        return this.currentFilterPreset
      } catch (error) {
        this.filterPresetsError = error.response?.data?.detail || error.message
        throw error
      } finally {
        this.filterPresetsLoading = false
      }
    },

    async createFilterPreset(presetData) {
      this.filterPresetsLoading = true
      this.filterPresetsError = null
      try {
        const response = await axios.post(`${API_BASE}/api/${API_VERSION}/analytics/filter-presets/`, presetData)
        this.filterPresets.push(response.data)
        return response.data
      } catch (error) {
        this.filterPresetsError = error.response?.data || error.message
        throw error
      } finally {
        this.filterPresetsLoading = false
      }
    },

    async updateFilterPreset(id, presetData) {
      this.filterPresetsLoading = true
      this.filterPresetsError = null
      try {
        const response = await axios.put(`${API_BASE}/api/${API_VERSION}/analytics/filter-presets/${id}/`, presetData)
        const index = this.filterPresets.findIndex(fp => fp.id === id)
        if (index !== -1) {
          this.filterPresets[index] = response.data
        }
        return response.data
      } catch (error) {
        this.filterPresetsError = error.response?.data || error.message
        throw error
      } finally {
        this.filterPresetsLoading = false
      }
    },

    async deleteFilterPreset(id) {
      this.filterPresetsLoading = true
      this.filterPresetsError = null
      try {
        await axios.delete(`${API_BASE}/api/${API_VERSION}/analytics/filter-presets/${id}/`)
        this.filterPresets = this.filterPresets.filter(fp => fp.id !== id)
      } catch (error) {
        this.filterPresetsError = error.response?.data?.detail || error.message
        throw error
      } finally {
        this.filterPresetsLoading = false
      }
    },

    // ==================== FORECAST MODELS ====================
    async fetchForecastModels(params = {}) {
      this.forecastModelsLoading = true
      this.forecastModelsError = null
      try {
        const response = await axios.get(`${API_BASE}/api/${API_VERSION}/analytics/forecast-models/`, { params })
        this.forecastModels = response.data.results || response.data
        return this.forecastModels
      } catch (error) {
        this.forecastModelsError = error.response?.data?.detail || error.message
        throw error
      } finally {
        this.forecastModelsLoading = false
      }
    },

    async fetchForecastModel(id) {
      this.forecastModelsLoading = true
      this.forecastModelsError = null
      try {
        const response = await axios.get(`${API_BASE}/api/${API_VERSION}/analytics/forecast-models/${id}/`)
        this.currentForecastModel = response.data
        return this.currentForecastModel
      } catch (error) {
        this.forecastModelsError = error.response?.data?.detail || error.message
        throw error
      } finally {
        this.forecastModelsLoading = false
      }
    },

    async createForecastModel(modelData) {
      this.forecastModelsLoading = true
      this.forecastModelsError = null
      try {
        const response = await axios.post(`${API_BASE}/api/${API_VERSION}/analytics/forecast-models/`, modelData)
        this.forecastModels.push(response.data)
        return response.data
      } catch (error) {
        this.forecastModelsError = error.response?.data || error.message
        throw error
      } finally {
        this.forecastModelsLoading = false
      }
    },

    async updateForecastModel(id, modelData) {
      this.forecastModelsLoading = true
      this.forecastModelsError = null
      try {
        const response = await axios.put(`${API_BASE}/api/${API_VERSION}/analytics/forecast-models/${id}/`, modelData)
        const index = this.forecastModels.findIndex(fm => fm.id === id)
        if (index !== -1) {
          this.forecastModels[index] = response.data
        }
        return response.data
      } catch (error) {
        this.forecastModelsError = error.response?.data || error.message
        throw error
      } finally {
        this.forecastModelsLoading = false
      }
    },

    async deleteForecastModel(id) {
      this.forecastModelsLoading = true
      this.forecastModelsError = null
      try {
        await axios.delete(`${API_BASE}/api/${API_VERSION}/analytics/forecast-models/${id}/`)
        this.forecastModels = this.forecastModels.filter(fm => fm.id !== id)
      } catch (error) {
        this.forecastModelsError = error.response?.data?.detail || error.message
        throw error
      } finally {
        this.forecastModelsLoading = false
      }
    },
  },
})
