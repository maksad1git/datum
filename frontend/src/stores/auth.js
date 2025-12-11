import { defineStore } from 'pinia'
import axios from 'axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('access_token') || null,
    refreshToken: localStorage.getItem('refresh_token') || null,
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
    currentUser: (state) => state.user,
  },

  actions: {
    async login(username, password) {
      try {
        const response = await axios.post('http://127.0.0.1:8000/api/auth/token/', {
          username,
          password
        })

        this.token = response.data.access
        this.refreshToken = response.data.refresh

        // Save to localStorage
        localStorage.setItem('access_token', this.token)
        localStorage.setItem('refresh_token', this.refreshToken)

        // Set default Authorization header
        axios.defaults.headers.common['Authorization'] = `Bearer ${this.token}`

        // Fetch user data
        await this.fetchUser()

        return { success: true }
      } catch (error) {
        console.error('Login failed:', error)
        return {
          success: false,
          message: error.response?.data?.detail || 'Login failed'
        }
      }
    },

    async fetchUser() {
      try {
        // TODO: Create user profile endpoint
        // For now, decode JWT to get user info
        const payload = JSON.parse(atob(this.token.split('.')[1]))
        this.user = {
          id: payload.user_id,
          username: payload.username || 'User'
        }
      } catch (error) {
        console.error('Failed to fetch user:', error)
      }
    },

    async refreshAccessToken() {
      try {
        const response = await axios.post('http://127.0.0.1:8000/api/auth/token/refresh/', {
          refresh: this.refreshToken
        })

        this.token = response.data.access
        localStorage.setItem('access_token', this.token)
        axios.defaults.headers.common['Authorization'] = `Bearer ${this.token}`

        return true
      } catch (error) {
        console.error('Token refresh failed:', error)
        this.logout()
        return false
      }
    },

    logout() {
      this.user = null
      this.token = null
      this.refreshToken = null

      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      delete axios.defaults.headers.common['Authorization']
    },

    initializeAuth() {
      if (this.token) {
        axios.defaults.headers.common['Authorization'] = `Bearer ${this.token}`
        this.fetchUser()
      }
    }
  }
})
