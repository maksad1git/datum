import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

// Set base URL
axios.defaults.baseURL = 'http://127.0.0.1:8000'

// Request interceptor
axios.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore()
    if (authStore.token) {
      config.headers.Authorization = `Bearer ${authStore.token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
axios.interceptors.response.use(
  (response) => {
    return response
  },
  async (error) => {
    const originalRequest = error.config

    // If 401 and not already retrying, try to refresh token
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      const authStore = useAuthStore()
      const refreshed = await authStore.refreshAccessToken()

      if (refreshed) {
        // Retry original request with new token
        return axios(originalRequest)
      } else {
        // Redirect to login
        window.location.href = '/login'
        return Promise.reject(error)
      }
    }

    return Promise.reject(error)
  }
)

export default axios
