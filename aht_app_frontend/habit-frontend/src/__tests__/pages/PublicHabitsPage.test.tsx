import { render, screen } from "@testing-library/react";
import PublicHabitsPage from "../../pages/PublicHabitsPage";
import { BrowserRouter } from "react-router-dom";
import { server } from "../../tests/msw/server";
import { http, HttpResponse } from "msw";

const API_URL = "http://127.0.0.1:8000/api/habits/public/";

test("public page lists public habits", async () => {
  server.use(
    http.get(API_URL, () =>
      HttpResponse.json([
        {
          id: 1,
          action: "Run",
          place: "Park",
          time_of_day: "Morning",
          is_pleasant: false,
          related_pleasant_habit: null,
          reward_text: null,
          periodicity_days: 1,
          repeat_limit: 30,
          grace_minutes: 0,
          fix_minutes: 0,
          is_public: true,
          is_active: true,
          created_at: "2025-01-01T00:00:00Z",
        },
      ])
    )
  );

  render(
    <BrowserRouter>
      <PublicHabitsPage />
    </BrowserRouter>
  );

  expect(await screen.findByText(/run/i)).toBeInTheDocument();
});
