import { apiClient } from "./apiClient";
import type { Habit, HabitCreateData } from "../types/Habit";
import type { HabitInstanceFilters } from "../types/HabitInstance";
import type { HabitStats } from "../types/HabitStats";

export const habitsApi = {
  getHabits() {
    return apiClient.get<Habit[]>("/habits/");
  },

  pleasant() {
    return apiClient.get("/habits/", { params: { is_pleasant: true } });
  },

  getHabit(id: number) {
    return apiClient.get<Habit>(`/habits/${id}/`);
  },

  createHabit(data: HabitCreateData) {
    return apiClient.post<Habit>("/habits/", data);
  },

  updateHabit(id: number, data: Partial<HabitCreateData>) {
    return apiClient.patch<Habit>(`/habits/${id}/`, data);
  },

  deleteHabit(id: number) {
    return apiClient.delete(`/habits/${id}/`);
  },

  details(id: number) {
    return apiClient.get(`/habits/${id}/details/`);
  },

  instances(habitId: number, params?: HabitInstanceFilters) {
    return apiClient.get(`/habits/${habitId}/instances/`, { params });
  },

  instancesForToday() {
    return apiClient.get("/habits/instances/today/");
  },

  stats(habitId: number) {
    return apiClient.get<HabitStats>(`/habits/${habitId}/stats/`);
  },

  getPleasantHabits() {
    return apiClient.get<Habit[]>("/habits/?is_pleasant=true");
  },

  publicHabits() {
    return apiClient.get("/habits/public/");
  },
};
