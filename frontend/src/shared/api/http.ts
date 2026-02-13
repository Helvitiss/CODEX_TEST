import axios from 'axios';
import { env } from '@/shared/config/env';
import { authTokenStore } from '@/shared/providers/AuthProvider';

export const http = axios.create({
  baseURL: env.apiUrl,
  headers: {
    'Content-Type': 'application/json'
  }
});

http.interceptors.request.use((config) => {
  const token = authTokenStore.getToken();
  if (token) {
    config.headers = config.headers ?? {};
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
