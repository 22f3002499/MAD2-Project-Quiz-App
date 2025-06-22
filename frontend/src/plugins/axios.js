import axios from "axios";

const apiClient = axios.create({
  baseURL:import.meta.env.VITE_BASE_URL || 'http://localhost:5000',
  timeout:10000,
  headers:{
    'Content-Type':'application/json',
    'Accept':'application/json'
  }
})

apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token")
    if (token){
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error)=>{
    console.log('Request error:' , error)
    return Promise.reject(error)
  }
)

export default apiClient

