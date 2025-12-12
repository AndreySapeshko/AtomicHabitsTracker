import { apiClient } from "./apiClient";

export const authApi = {
  register(data: { email: string; password: string }) {
    return apiClient.post("auth/register/", data);
  },
  login(data: { email: string; password: string }) {
    return apiClient.post("auth/login/", data);
  },
  me() {
    return apiClient.get("auth/me/");
  },
  generateBindCode() {
    return apiClient.post("telegram/create_binding/");
  },
};
