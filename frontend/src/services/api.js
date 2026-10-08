import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_URL || '/api';

const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const resumeApi = {
  uploadFile: (file) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post('/resumes/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
  uploadText: (text, fileName) => api.post('/resumes/text', { text, fileName }),
  getAll: () => api.get('/resumes'),
  getById: (id) => api.get(`/resumes/${id}`),
};

export const jobApi = {
  create: (jobData) => api.post('/jobs', jobData),
  getAll: () => api.get('/jobs'),
  getById: (id) => api.get(`/jobs/${id}`),
};

export const analysisApi = {
  runAnalysis: (data) => api.post('/analyses/run', data),
  roleFit: (data) => api.post('/analyses/role-fit', data),
  getAll: () => api.get('/analyses'),
  getById: (id) => api.get(`/analyses/${id}`),
};

export const interviewApi = {
  start: (data) => api.post('/interview/start', data),
  respond: (data) => api.post('/interview/respond', data),
  roleQuestions: (data) => api.post('/interview/questions', data),
  evaluate: (data) => api.post('/interview/evaluate', data),
};

export const healthApi = {
  check: () => api.get('/health'),
};

export default api;
