import { ref, computed , readonly} from 'vue'
import apiClient from '@/plugins/axios'

export function useApi() {
  const loading = ref(false)
  const error = ref(null)

  const isLoading = computed(() => loading.value)
  const hasError = computed(() => error.value !== null)

  const execute = async (requestConfig) => {
    try {
      loading.value = true
      error.value = null
      
      const response = await apiClient(requestConfig)
      
      return response.data
    } catch (err) {
      error.value = err.response?.data || err.response?.data?.message || err.message || 'An error occurred'
      console.log(err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const get = (url, config = {}) => execute({ method: 'GET', url, ...config })
  const post = (url, data, config = {}) => execute({ method: 'POST', url, data, ...config })
  const put = (url, data, config = {}) => execute({ method: 'PUT', url, data, ...config })
  const patch = (url, data, config = {}) => execute({ method: 'PATCH', url, data, ...config })
  const del = (url, config = {}) => execute({ method: 'DELETE', url, ...config })

  const reset = () => {
    loading.value = false
    error.value = null
  }

  return {
    loading: readonly(loading),
    error: readonly(error),
    
    isLoading,
    hasError,
    
    execute,
    get,
    post,
    put,
    patch,
    del,
    reset
  }
}
