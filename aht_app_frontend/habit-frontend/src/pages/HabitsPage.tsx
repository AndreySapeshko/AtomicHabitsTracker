import { useEffect, useState, useCallback } from "react";
import { habitsApi } from "../api/habitsApi";
import type { Habit } from "../types/Habit";
import { Link } from "react-router-dom";
import { HabitCard } from "../components/HabitCard";

export default function HabitsPage() {
  const [habits, setHabits] = useState<Habit[]>([]);
  const [error, setError] = useState<string | null>(null);

  const loadHabits = useCallback(async () => {
    try {
      const res = await habitsApi.getHabits();
      setHabits(res.data);
    } catch {
      setError("Не удалось загрузить привычки");
    }
  }, []);

  useEffect(() => {
    (async () => {
      await loadHabits();
    })();
  }, [loadHabits]);

  if (error) return <div style={{ padding: 20 }}>{error}</div>;

  return (
    <div style={{ padding: 20, maxWidth: 900, margin: "0 auto" }}>
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          marginBottom: 20,
        }}
      >
        <h2>Мои привычки</h2>

        <Link to="/habits/create">
          <button style={{ padding: "8px 16px" }}>➕ Новая привычка</button>
        </Link>
      </div>

      {habits.length === 0 ? (
        <p>У вас пока нет привычек. Создайте первую!</p>
      ) : (
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(250px, 1fr))",
            gap: 16,
          }}
        >
          {habits.map((h) => (
            <HabitCard key={h.id} habit={h} />
          ))}
        </div>
      )}
    </div>
  );
}
