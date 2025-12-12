import { defineStore } from 'pinia'
import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'
const API_VERSION = import.meta.env.VITE_API_VERSION || 'v1'

export const useUsersStore = defineStore('users', {
  state: () => ({
    // Users
    users: [],
    currentUser: null,

    // Roles
    roles: [],
    currentRole: null,

    // Permissions
    permissions: [],
    currentPermission: null,

    // Sessions
    sessions: [],
    currentSession: null,

    // Loading states
    usersLoading: false,
    rolesLoading: false,
    permissionsLoading: false,
    sessionsLoading: false,

    // Error states
    usersError: null,
    rolesError: null,
    permissionsError: null,
    sessionsError: null,
  }),

  getters: {
    // User getters
    activeUsers: (state) => state.users.filter(u => u.is_active),
    userById: (state) => (id) => state.users.find(u => u.id === id),
    usersByRole: (state) => (roleId) => state.users.filter(u => u.role === roleId),

    // Role getters
    activeRoles: (state) => state.roles.filter(r => r.is_active),
    roleById: (state) => (id) => state.roles.find(r => r.id === id),

    // Permission getters
    permissionById: (state) => (id) => state.permissions.find(p => p.id === id),

    // Session getters
    activeSessions: (state) => state.sessions.filter(s => s.is_active),
    sessionById: (state) => (id) => state.sessions.find(s => s.id === id),
    sessionsByUser: (state) => (userId) => state.sessions.filter(s => s.user === userId),
  },

  actions: {
    // ==================== USERS ====================
    async fetchUsers(params = {}) {
      this.usersLoading = true
      this.usersError = null
      try {
        const response = await axios.get(`${API_BASE}/api/${API_VERSION}/users/users/`, { params })
        this.users = response.data.results || response.data
        return this.users
      } catch (error) {
        this.usersError = error.response?.data?.detail || error.message
        throw error
      } finally {
        this.usersLoading = false
      }
    },

    async fetchUser(id) {
      this.usersLoading = true
      this.usersError = null
      try {
        const response = await axios.get(`${API_BASE}/api/${API_VERSION}/users/users/${id}/`)
        this.currentUser = response.data
        return this.currentUser
      } catch (error) {
        this.usersError = error.response?.data?.detail || error.message
        throw error
      } finally {
        this.usersLoading = false
      }
    },

    async createUser(userData) {
      this.usersLoading = true
      this.usersError = null
      try {
        const response = await axios.post(`${API_BASE}/api/${API_VERSION}/users/users/`, userData)
        this.users.push(response.data)
        return response.data
      } catch (error) {
        this.usersError = error.response?.data || error.message
        throw error
      } finally {
        this.usersLoading = false
      }
    },

    async updateUser(id, userData) {
      this.usersLoading = true
      this.usersError = null
      try {
        const response = await axios.put(`${API_BASE}/api/${API_VERSION}/users/users/${id}/`, userData)
        const index = this.users.findIndex(u => u.id === id)
        if (index !== -1) {
          this.users[index] = response.data
        }
        return response.data
      } catch (error) {
        this.usersError = error.response?.data || error.message
        throw error
      } finally {
        this.usersLoading = false
      }
    },

    async deleteUser(id) {
      this.usersLoading = true
      this.usersError = null
      try {
        await axios.delete(`${API_BASE}/api/${API_VERSION}/users/users/${id}/`)
        this.users = this.users.filter(u => u.id !== id)
      } catch (error) {
        this.usersError = error.response?.data?.detail || error.message
        throw error
      } finally {
        this.usersLoading = false
      }
    },

    // ==================== ROLES ====================
    async fetchRoles(params = {}) {
      this.rolesLoading = true
      this.rolesError = null
      try {
        const response = await axios.get(`${API_BASE}/api/${API_VERSION}/users/roles/`, { params })
        this.roles = response.data.results || response.data
        return this.roles
      } catch (error) {
        this.rolesError = error.response?.data?.detail || error.message
        throw error
      } finally {
        this.rolesLoading = false
      }
    },

    async fetchRole(id) {
      this.rolesLoading = true
      this.rolesError = null
      try {
        const response = await axios.get(`${API_BASE}/api/${API_VERSION}/users/roles/${id}/`)
        this.currentRole = response.data
        return this.currentRole
      } catch (error) {
        this.rolesError = error.response?.data?.detail || error.message
        throw error
      } finally {
        this.rolesLoading = false
      }
    },

    async createRole(roleData) {
      this.rolesLoading = true
      this.rolesError = null
      try {
        const response = await axios.post(`${API_BASE}/api/${API_VERSION}/users/roles/`, roleData)
        this.roles.push(response.data)
        return response.data
      } catch (error) {
        this.rolesError = error.response?.data || error.message
        throw error
      } finally {
        this.rolesLoading = false
      }
    },

    async updateRole(id, roleData) {
      this.rolesLoading = true
      this.rolesError = null
      try {
        const response = await axios.put(`${API_BASE}/api/${API_VERSION}/users/roles/${id}/`, roleData)
        const index = this.roles.findIndex(r => r.id === id)
        if (index !== -1) {
          this.roles[index] = response.data
        }
        return response.data
      } catch (error) {
        this.rolesError = error.response?.data || error.message
        throw error
      } finally {
        this.rolesLoading = false
      }
    },

    async deleteRole(id) {
      this.rolesLoading = true
      this.rolesError = null
      try {
        await axios.delete(`${API_BASE}/api/${API_VERSION}/users/roles/${id}/`)
        this.roles = this.roles.filter(r => r.id !== id)
      } catch (error) {
        this.rolesError = error.response?.data?.detail || error.message
        throw error
      } finally {
        this.rolesLoading = false
      }
    },

    // ==================== PERMISSIONS ====================
    async fetchPermissions(params = {}) {
      this.permissionsLoading = true
      this.permissionsError = null
      try {
        const response = await axios.get(`${API_BASE}/api/${API_VERSION}/users/permissions/`, { params })
        this.permissions = response.data.results || response.data
        return this.permissions
      } catch (error) {
        this.permissionsError = error.response?.data?.detail || error.message
        throw error
      } finally {
        this.permissionsLoading = false
      }
    },

    async fetchPermission(id) {
      this.permissionsLoading = true
      this.permissionsError = null
      try {
        const response = await axios.get(`${API_BASE}/api/${API_VERSION}/users/permissions/${id}/`)
        this.currentPermission = response.data
        return this.currentPermission
      } catch (error) {
        this.permissionsError = error.response?.data?.detail || error.message
        throw error
      } finally {
        this.permissionsLoading = false
      }
    },

    async createPermission(permissionData) {
      this.permissionsLoading = true
      this.permissionsError = null
      try {
        const response = await axios.post(`${API_BASE}/api/${API_VERSION}/users/permissions/`, permissionData)
        this.permissions.push(response.data)
        return response.data
      } catch (error) {
        this.permissionsError = error.response?.data || error.message
        throw error
      } finally {
        this.permissionsLoading = false
      }
    },

    async updatePermission(id, permissionData) {
      this.permissionsLoading = true
      this.permissionsError = null
      try {
        const response = await axios.put(`${API_BASE}/api/${API_VERSION}/users/permissions/${id}/`, permissionData)
        const index = this.permissions.findIndex(p => p.id === id)
        if (index !== -1) {
          this.permissions[index] = response.data
        }
        return response.data
      } catch (error) {
        this.permissionsError = error.response?.data || error.message
        throw error
      } finally {
        this.permissionsLoading = false
      }
    },

    async deletePermission(id) {
      this.permissionsLoading = true
      this.permissionsError = null
      try {
        await axios.delete(`${API_BASE}/api/${API_VERSION}/users/permissions/${id}/`)
        this.permissions = this.permissions.filter(p => p.id !== id)
      } catch (error) {
        this.permissionsError = error.response?.data?.detail || error.message
        throw error
      } finally {
        this.permissionsLoading = false
      }
    },

    // ==================== SESSIONS ====================
    async fetchSessions(params = {}) {
      this.sessionsLoading = true
      this.sessionsError = null
      try {
        const response = await axios.get(`${API_BASE}/api/${API_VERSION}/users/sessions/`, { params })
        this.sessions = response.data.results || response.data
        return this.sessions
      } catch (error) {
        this.sessionsError = error.response?.data?.detail || error.message
        throw error
      } finally {
        this.sessionsLoading = false
      }
    },

    async fetchSession(id) {
      this.sessionsLoading = true
      this.sessionsError = null
      try {
        const response = await axios.get(`${API_BASE}/api/${API_VERSION}/users/sessions/${id}/`)
        this.currentSession = response.data
        return this.currentSession
      } catch (error) {
        this.sessionsError = error.response?.data?.detail || error.message
        throw error
      } finally {
        this.sessionsLoading = false
      }
    },

    async deleteSession(id) {
      this.sessionsLoading = true
      this.sessionsError = null
      try {
        await axios.delete(`${API_BASE}/api/${API_VERSION}/users/sessions/${id}/`)
        this.sessions = this.sessions.filter(s => s.id !== id)
      } catch (error) {
        this.sessionsError = error.response?.data?.detail || error.message
        throw error
      } finally {
        this.sessionsLoading = false
      }
    },
  },
})
