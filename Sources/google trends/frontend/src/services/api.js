import axios from 'axios';

// Define base API URL
const BASE_URL = process.env.REACT_APP_API_URL || '/api';

// Create axios instance
const api = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});

// API services object
const apiService = {
  // Trends API
  trends: {
    // Get current trending topics
    getCurrent: (params = {}) => {
      return api.get('/trends/current', { params });
    },
    
    // Search for specific keywords
    search: (params = {}) => {
      return api.get('/trends/search', { params });
    },
    
    // Get regional trends
    getRegional: (region, params = {}) => {
      return api.get(`/trends/geographic/${region}`, { params });
    },
    
    // Get historical trend data
    getHistory: (params = {}) => {
      return api.get('/trends/history', { params });
    }
  },
  
  // Content API
  content: {
    // Generate content suggestions
    generateSuggestions: (data) => {
      return api.post('/content/suggestions', data);
    },
    
    // Generate bulk content suggestions
    generateBulkSuggestions: (data) => {
      return api.post('/content/suggestions/bulk', data);
    },
    
    // Generate content suggestions for trending topics
    generateTrendingSuggestions: (params = {}) => {
      return api.get('/content/suggestions/trending', { params });
    }
  }
};

export default apiService; 