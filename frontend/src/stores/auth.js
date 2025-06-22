import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { jwtDecode } from 'jwt-decode' 

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || null)
  const userDetails = computed(() => {
    if (!token.value) return null
    try {
      return jwtDecode(token.value)
    } catch {
      return null
    }
  })
  const isAuthenticated = computed(() => !!token.value)
  const userRole = computed(() => userDetails.value?.role)
  const hasRole = (role) => userRole.value === role
  const hasAnyRole = (roles) => roles.includes(userRole.value) 
  
  const setToken = (newToken) => {
    token.value = newToken
    localStorage.setItem('token', newToken)
  }
  
  const logout = () => {
    token.value = null
    localStorage.removeItem('token')
  }
  
  return { token, userDetails, isAuthenticated, userRole, hasRole, hasAnyRole, setToken, logout }
})
