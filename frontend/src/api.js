import axios from 'axios';

const api = axios.create({
  //baseURL: "http://127.0.0.1:8000"
  baseURL: "http://localhost:8000"
});

export const fetchAllLocations = () => api.get('/locations/all/');

export default api;
