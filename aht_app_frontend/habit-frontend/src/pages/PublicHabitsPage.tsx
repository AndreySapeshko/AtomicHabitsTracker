import { useEffect, useState, useCallback } from "react";
import { habitsApi } from "../api/habitsApi";
import type { Habit } from "../types/Habit";
import { PublicHabitCard } from "../components/PublicHabitCard";

export default function PublicHabitsPage() {
  const [habits, setHabits] = useState<Habit[]>([]);
  const [error, setError] = useState<string | null>(null);

  const loadPublicHabits = useCallback(async () => {
    try {
      const res = await habitsApi.publicHabits();
      setHabits(res.data);
    } catch (err) {
      console.error(err);
      setError("Не удалось загрузить публичные привычки");
    }
  }, []);

  useEffect(() => {
    (async () => {
      await loadPublicHabits();
    })();
  }, [loadPublicHabits]);

  if (error) return <div style={{ padding: 20 }}>{error}</div>;

  return (
    <div style={{ padding: 20, maxWidth: 900, margin: "0 auto" }}>
      <h2>Публичные привычки</h2>
      <p>Здесь вы можете посмотреть привычки других пользователей.</p>

      {habits.length === 0 ? (
        <p>Пока нет публичных привычек.</p>
      ) : (
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(250px, 1fr))",
            gap: 16,
          }}
        >
          {habits.map((h) => (
            <PublicHabitCard key={h.id} habit={h} />
          ))}
        </div>
      )}
    </div>
  );
}
