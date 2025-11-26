import api from './api';

export const jobService = {
  getAllJobs: async (filters) => {
    const response = await api.get('/jobs', { params: filters });
    return response.data;
  },
  
  getJobById: async (id) => {
    const response = await api.get(`/jobs/${id}`);
    return response.data;
  },
  
  createJob: async (jobData) => {
    const response = await api.post('/jobs', jobData);
    return response.data;
  },
  
  applyForJob: async (jobId, applicationData) => {
    const response = await api.post(`/jobs/${jobId}/apply`, applicationData);
    return response.data;
  }
};

// frontend/src/services/authService.js
import api from './api';

export const authService = {
  login: async (credentials) => {
    const response = await api.post('/auth/login', credentials);
    if (response.data.token) {
      localStorage.setItem('token', response.data.token);
    }
    return response.data;
  },
  
  register: async (userData) => {
    const response = await api.post('/auth/register', userData);
    return response.data;
  },
  
  logout: () => {
    localStorage.removeItem('token');
  }
};