import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import HabitsPage from "../../pages/HabitsPage";
import { server } from "../../tests/msw/server";
import { http, HttpResponse } from "msw";

describe("HabitsPage", () => {
  test("отображает привычки, полученные с сервера", async () => {
    server.use(
      http.get("http://127.0.0.1:8000/api/habits*", () =>
        HttpResponse.json([
          {
            id: 1,
            action: "Привычка 1",
            place: "",
            time_of_day: "",
            is_pleasant: false,
            related_pleasant_habit: null,
            reward_text: null,
            periodicity_days: 1,
            repeat_limit: 21,
            grace_minutes: 0,
            fix_minutes: 0,
            is_public: false,
            is_active: true,
            created_at: "",
          },
          {
            id: 2,
            action: "Привычка 2",
            place: "",
            time_of_day: "",
            is_pleasant: false,
            related_pleasant_habit: null,
            reward_text: null,
            periodicity_days: 1,
            repeat_limit: 21,
            grace_minutes: 0,
            fix_minutes: 0,
            is_public: false,
            is_active: true,
            created_at: "",
          },
        ]),
      ),
    );

    render(
      <MemoryRouter>
        <HabitsPage />
      </MemoryRouter>,
    );

    // Теперь точно найдётся
    expect(await screen.findByText(/Привычка 1/i)).toBeInTheDocument();
    expect(screen.getByText(/Привычка 2/i)).toBeInTheDocument();
  });
});
