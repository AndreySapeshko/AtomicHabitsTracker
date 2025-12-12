import { http, HttpResponse } from "msw";
import { mockHabitStats } from "../../__tests__/mocks/habitStats.mock";
import { mockHabitDetails } from "../../__tests__/mocks/habitDetails.mock";


export const handlers = [

  // Auth
  http.post("/auth/login", async () => {
    return HttpResponse.json({
      access: "fake-jwt",
      refresh: "fake-refresh",
      user: { id: 1, email: "test@mail.com" }
    });
  }),

  http.get("/auth/me", async () => {
    return HttpResponse.json({
      id: 1,
      email: "test@mail.com"
    });
  }),

  // Habits
  http.get("/habits", async () => {
    return HttpResponse.json([
      { id: 1, action: "Drink water", is_public: false },
      { id: 2, action: "Stretch", is_public: true },
    ]);
  }),

  http.get("/habits/1", async () => {
    return HttpResponse.json({
      id: 1,
      action: "Drink water",
      place: "Home",
      time_of_day: "morning",
      periodicity_days: 1,
      is_public: false,
    });
  }),

  // Today
  http.get("/today", async () => {
    return HttpResponse.json([
      {
        id: 55,
        scheduled: "10:00",
        habit: { action: "Meditate" }
      },
    ]);
  }),

  // Public habits
  http.get("/public", async () => {
    return HttpResponse.json([
      { id: 10, action: "Run", username: "john" },
    ]);
  }),

  // Analytics
  http.get("http://127.0.0.1:8000/api/habits/:id/stats/", () => {
    return HttpResponse.json(mockHabitStats);
  }),

  // Details
  http.get("http://127.0.0.1:8000/api/habits/:id/details/", () => {
    return HttpResponse.json(mockHabitDetails);
  }),
];
