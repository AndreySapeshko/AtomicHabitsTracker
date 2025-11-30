import { apiClient } from "./apiClient";
import type { Habit, HabitCreateData } from "../types/Habit";

export const habitsApi = {
  getHabits() {
    return apiClient.get<Habit[]>("/habits/");
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

  getPleasantHabits() {
    return apiClient.get<Habit[]>("/habits/?is_pleasant=true");
  },
};
