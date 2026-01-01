import axios from 'axios'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || ''

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 seconds timeout
})

// API Service Functions
export const emailApi = {
  // Generate initial email draft
  generateDraft: async (topic) => {
    try {
      const response = await api.post('/api/generate', { topic })
      return response.data
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to generate email')
    }
  },

  // Process feedback and regenerate
  processFeedback: async (sessionId, feedback) => {
    try {
      const response = await api.post('/api/feedback', {
        session_id: sessionId,
        feedback,
      })
      return response.data
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to process feedback')
    }
  },

  // Finalize email draft
  finalizeDraft: async (sessionId) => {
    try {
      const response = await api.post('/api/finalize', {
        session_id: sessionId,
      })
      return response.data
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to finalize email')
    }
  },

  // Send email
  sendEmail: async (sessionId, email) => {
    try {
      const response = await api.post('/api/send-email', {
        session_id: sessionId,
        email,
      })
      return response.data
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to send email')
    }
  },

  // Get session details
  getSession: async (sessionId) => {
    try {
      const response = await api.get(`/api/session/${sessionId}`)
      return response.data
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to fetch session')
    }
  },

  // Health check
  healthCheck: async () => {
    try {
      const response = await api.get('/health')
      return response.data
    } catch (firstError) {
      try {
        const response = await api.get('/api/health')
        return response.data
      } catch (secondError) {
        throw new Error('Backend service is unavailable')
      }
    }
  },
}

export default api
