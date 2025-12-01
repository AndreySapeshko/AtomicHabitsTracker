import { Link } from "react-router-dom";
import { Card } from "./Card";
import type { Habit } from "../types/Habit";

interface Props {
  habit: Habit;
}

export function HabitCard({ habit }: Props) {
  return (
    <Card>
      <div style={{ display: "flex", justifyContent: "space-between" }}>
        <h3>{habit.action}</h3>

        <span
          style={{
            padding: "4px 8px",
            borderRadius: 6,
            background: habit.is_active ? "#e0f7e9" : "#ffe4e4",
            color: habit.is_active ? "#0a7d38" : "#c62828",
            fontSize: 12,
            height: 20,
          }}
        >
          {habit.is_active ? "Активна" : "Неактивна"}
        </span>
      </div>

      <p style={{ marginTop: 8, marginBottom: 8 }}>
        <b>Место:</b> {habit.place}
      </p>
      <p style={{ marginTop: 0, marginBottom: 8 }}>
        <b>Тип:</b> {habit.is_pleasant ? "Приятная" : "Полезная"}
      </p>
      <p style={{ marginTop: 0, marginBottom: 8 }}>
        <b>Периодичность:</b> каждые {habit.periodicity_days} дней
      </p>

      {!habit.is_pleasant && (
        <p style={{ marginTop: 0, marginBottom: 8 }}>
          <b>Время:</b> {habit.time_of_day}
        </p>
      )}

      <div style={{ display: "flex", gap: 10, marginTop: 15 }}>
        <Link to={`/habits/${habit.id}`}>
          <button>Подробнее</button>
        </Link>

        <Link to={`/habits/${habit.id}/analytics`}>
          <button>📊 Аналитика</button>
        </Link>

        <Link to={`/habits/${habit.id}/edit`}>
          <button>✏ Редактировать</button>
        </Link>
      </div>
    </Card>
  );
}
