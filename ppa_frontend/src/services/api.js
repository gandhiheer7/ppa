import axios from 'axios';

const api = axios.create({
    baseURL: 'http://127.0.0.1:5000/api', // Points to your Flask backend
    headers: {
        'Content-Type': 'application/json'
    }
});

// Request interceptor to add the JWT token to headers
api.interceptors.request.use(config => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
}, error => {
    return Promise.reject(error);
});

export default api;