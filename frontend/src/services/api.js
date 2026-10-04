import axios from 'axios';

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const movieApi = {
  getMovies: (params) => api.get('/movies', { params }),
  getMovieById: (id) => api.get(`/movies/${id}`),
  searchMovies: (q) => api.get('/movies/search', { params: { q } }),
  getGenres: () => api.get('/genres'),
};

export const userApi = {
  getUsers: () => api.get('/users'),
  getUserById: (id) => api.get(`/users/${id}`),
  getUserRatings: (id) => api.get(`/users/${id}/ratings`),
  getUserGenrePreferences: (id) => api.get(`/users/${id}/genre-preferences`),
};

export const ratingApi = {
  addRating: (data) => api.post('/ratings', data),
  addWatchHistory: (data) => api.post('/watch-history', data),
};

export const recommendationApi = {
  getRecommendations: (userId, topN = 8) => api.get(`/recommendations/${userId}`, { params: { top_n: topN } }),
  getContentBased: (data) => api.post('/recommendations/content-based', data),
  getCollaborative: (data) => api.post('/recommendations/collaborative', data),
};

export const miningApi = {
  getStatistics: () => api.get('/mining/statistics'),
  getClusters: () => api.get('/mining/clusters'),
  runClustering: (k) => api.post('/mining/cluster-users', { k }),
  getAssociationRules: () => api.get('/mining/association-rules'),
  runAssociationRules: (params) => api.post('/mining/association-rules', params),
  classifyPreference: (userId, movieId) => api.post('/mining/classify-preference', { user_id: userId, movie_id: movieId }),
  runPipeline: () => api.post('/mining/pipeline/run-all'),
};

export default api;
