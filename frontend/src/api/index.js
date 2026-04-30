import axios from "axios";

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000",
  timeout: 10000,
  headers: {
    "Content-Type": "application/json",
  },
  paramsSerializer: (params) => {
    const searchParams = new URLSearchParams();
    for (const key in params) {
      if (Array.isArray(params[key])) {
        params[key].forEach((value) => searchParams.append(key, value));
      } else {
        searchParams.append(key, params[key]);
      }
    }
    return searchParams.toString();
  },
});

apiClient.interceptors.request.use(
  (config) => {
    return config;
  },
  (error) => {
    return Promise.reject(error);
  },
);

apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    console.error("API Error:", error.response?.data || error.message);
    return Promise.reject(error);
  },
);

export default apiClient;
