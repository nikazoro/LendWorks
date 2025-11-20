import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const api = axios.create({
    baseURL: `${API_BASE}/api/v1`,
    // ❌ remove withCredentials, you’re not using cookies
})

api.interceptors.request.use((config) => {
    const token = localStorage.getItem('token')
    if (token) {
        config.headers = {
            ...config.headers,
            Authorization: `Bearer ${token}`,
        }
    }
    return config
})

export default api
