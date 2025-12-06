import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { HabitCard } from "../../components/HabitCard";
import type { Habit } from "../../types/Habit";

function renderCard(habit: Habit, showActions = true) {
  return render(
    <MemoryRouter>
      <HabitCard habit={habit} showActions={showActions} />
    </MemoryRouter>
  );
}

const baseHabit: Habit = {
  id: 1,
  action: "Пробежка",
  place: "Парк",
  time_of_day: "утром",

  is_pleasant: false,
  related_pleasant_habit: null,
  reward_text: null,

  periodicity_days: 2,
  repeat_limit: 21,
  grace_minutes: 0,
  fix_minutes: 0,
  is_public: false,
  is_active: true,
  created_at: "2025-01-01T00:00:00Z",
};

describe("HabitCard", () => {
  test("рендерит данные привычки", () => {
    renderCard(baseHabit);

    expect(screen.getByText("💛 Пробежка")).toBeInTheDocument();
    expect(screen.getByText("Парк")).toBeInTheDocument();

    // Для обычной привычки должно быть время + периодичность
    expect(screen.getByText("⏰ утром • каждые 2 дн.")).toBeInTheDocument();

    // Статус
    expect(screen.getByText("Активна")).toBeInTheDocument();
  });

  test("рендерит вариант приятной привычки", () => {
    const pleasantHabit = {
      ...baseHabit,
      is_pleasant: true,
    };

    renderCard(pleasantHabit);

    expect(screen.getByText("💙 Пробежка")).toBeInTheDocument();

    // Должно показывать "Приятная привычка"
    expect(screen.getByText("Приятная привычка")).toBeInTheDocument();
  });

  test("показывает кнопки действий, если showActions=true", () => {
    renderCard(baseHabit, true);

    expect(screen.getByText("Подробнее")).toBeInTheDocument();
    expect(screen.getByText("📊 Аналитика")).toBeInTheDocument();
    expect(screen.getByText("✏ Редактировать")).toBeInTheDocument();
  });

  test("НЕ показывает кнопки действий, если showActions=false", () => {
    renderCard(baseHabit, false);

    expect(screen.queryByText("Подробнее")).toBeNull();
    expect(screen.queryByText("📊 Аналитика")).toBeNull();
    expect(screen.queryByText("✏ Редактировать")).toBeNull();
  });

  test("ссылки ведут на корректные маршруты", () => {
    renderCard(baseHabit);

    expect(
      (screen.getByText("Подробнее").closest("a") as HTMLAnchorElement).href
    ).toContain("/habits/1");

    expect(
      (screen.getByText("📊 Аналитика").closest("a") as HTMLAnchorElement).href
    ).toContain("/habits/1/analytics");

    expect(
      (screen.getByText("✏ Редактировать").closest("a") as HTMLAnchorElement).href
    ).toContain("/habits/1/edit");
  });

  test("отображает статус Неактивна", () => {
    const inactiveHabit = { ...baseHabit, is_active: false };
    renderCard(inactiveHabit);

    expect(screen.getByText("Неактивна")).toBeInTheDocument();
  });
});
