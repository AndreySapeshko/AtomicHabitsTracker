import axios, { AxiosError } from "axios";
import { useAuthStore } from "../store/authStore";
const baseURL = import.meta.env.VITE_API_URL;

export const apiClient = axios.create({
  baseURL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Добавляем access токен в каждый запрос, если он есть
apiClient.interceptors.request.use((config) => {
  const access = useAuthStore.getState().access;
  if (access) {
    config.headers = config.headers ?? {};
    config.headers.Authorization = `Bearer ${access}`;
  }
  return config;
});

// Базовая обработка 401 — вылогиниваем и отправляем на /login
apiClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    if (error.response?.status === 401) {
      useAuthStore.getState().logout();
      // простейший способ — редирект
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
);
