import { Link } from "react-router-dom";
import type { Habit } from "../types/Habit";
import { Card } from "./Card";
import { Button } from "./Button";

interface HabitCardProps {
  habit: Habit;
  showActions?: boolean;
}

export function HabitCard({ habit, showActions = true }: HabitCardProps) {
  const icon = habit.is_pleasant ? "💙" : "💛";

  return (
    <Card
      style={{
        display: "flex",
        flexDirection: "column",
        height: "100%",
      }}
    >
      <div style={{ marginBottom: 8 }}>
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            gap: 8,
            alignItems: "center",
          }}
        >
          <h3 style={{ margin: 0, fontSize: 16 }}>
            {icon} {habit.action}
          </h3>
          <span
            style={{
              padding: "2px 8px",
              borderRadius: 999,
              fontSize: 11,
              background: habit.is_active ? "#dcfce7" : "#fee2e2",
              color: habit.is_active ? "#166534" : "#b91c1c",
              whiteSpace: "nowrap",
            }}
          >
            {habit.is_active ? "Активна" : "Неактивна"}
          </span>
        </div>

        <p style={{ margin: "6px 0 4px", fontSize: 13, color: "#4b5563" }}>
          {habit.place}
        </p>

        {!habit.is_pleasant && (
          <p style={{ margin: 0, fontSize: 12, color: "#6b7280" }}>
            ⏰ {habit.time_of_day} • каждые {habit.periodicity_days} дн.
          </p>
        )}

        {habit.is_pleasant && (
          <p style={{ margin: 0, fontSize: 12, color: "#6b7280" }}>Приятная привычка</p>
        )}
      </div>

      {showActions && (
        <div
          style={{
            marginTop: "auto",
            display: "flex",
            gap: 8,
            flexWrap: "wrap",
          }}
        >
          <Link to={`/habits/${habit.id}`}>
            <Button variant="secondary">Подробнее</Button>
          </Link>
          <Link to={`/habits/${habit.id}/analytics`}>
            <Button variant="ghost">📊 Аналитика</Button>
          </Link>
          <Link to={`/habits/${habit.id}/edit`}>
            <Button variant="ghost">✏ Редактировать</Button>
          </Link>
        </div>
      )}
    </Card>
  );
}
