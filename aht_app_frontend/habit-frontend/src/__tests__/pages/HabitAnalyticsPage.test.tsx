import { render, screen, } from "@testing-library/react";
import { MemoryRouter, Routes, Route } from "react-router-dom";
import HabitAnalyticsPage from "../../pages/HabitAnalyticsPage";
import { server } from "../../tests/msw/server";
import { http, HttpResponse } from "msw";

// Моковые данные
const mockStats = {
  progress_percent: 75,
  repeat_limit: 3,
  current_streak: 5,
  max_streak: 10,
  total_completed: 20,
  total_missed: 3,
  total_pending: 2,
  per_week: [{ week: "2025-01-01", completed: 3, missed: 1 }],
  last_30_days: {
    "2025-02-01": "completed",
    "2025-02-02": "missed",
  },
};

const mockHabit = {
  habit: {
    action: "Drink water",
  },
};

// Подменяем API ответы перед каждым тестом
beforeEach(() => {
  server.use(
    http.get("http://127.0.0.1:8000/api/habits/:id/stats/", () =>
      HttpResponse.json(mockStats)
    ),

    http.get("http://127.0.0.1:8000/api/habits/:id/details/", () =>
      HttpResponse.json(mockHabit)
    )
  );
});

test("renders habit analytics data", async () => {
  render(
    <MemoryRouter initialEntries={["/habits/1/analytics"]}>
      <Routes>
        <Route path="/habits/:id/analytics" element={<HabitAnalyticsPage />} />
      </Routes>
    </MemoryRouter>
  );

  // 1. Проверяем, что сперва отображается "Загрузка..."
  expect(screen.getByText(/загрузка/i)).toBeInTheDocument();

  // 2. Дождаться загрузки данных
  const title = await screen.findByText((text) =>
  text.includes("Drink water")
);

  // 3. Проверяем ключевые элементы
  expect(title).toBeInTheDocument();
  expect(screen.getByText("🎯 Прогресс")).toBeInTheDocument();
  expect(screen.getByText(/текущий стрик/i)).toBeInTheDocument();
  expect(screen.getByText(/максимальный стрик/i)).toBeInTheDocument();
  expect(screen.getByText(/последние 30 дней/i)).toBeInTheDocument();

  // 4. Проверяем отображение значений
  expect(screen.getByText("5")).toBeInTheDocument(); // current streak
  expect(screen.getByText("10")).toBeInTheDocument(); // max streak
  //expect(screen.getByText("20")).toBeInTheDocument(); // completed
  expect(screen.getByText("3")).toBeInTheDocument(); // missed
});
