import { create } from "zustand";

export type AuthState = {
  access: string | null;
  refresh: string | null;

  setTokens: (access: string, refresh: string) => void;
  logout: () => void;
};

const ACCESS_KEY = "access_token";
const REFRESH_KEY = "refresh_token";

export const useAuthStore = create<AuthState>((set) => ({
  access: localStorage.getItem(ACCESS_KEY),
  refresh: localStorage.getItem(REFRESH_KEY),

  setTokens: (access, refresh) => {
    localStorage.setItem(ACCESS_KEY, access);
    localStorage.setItem(REFRESH_KEY, refresh);
    set({ access, refresh });
  },

  logout: () => {
    localStorage.removeItem(ACCESS_KEY);
    localStorage.removeItem(REFRESH_KEY);
    set({ access: null, refresh: null });
  },
}));
