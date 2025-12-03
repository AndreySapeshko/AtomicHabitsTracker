import { useCallback, useEffect, useState } from "react";
import { habitsApi } from "../api/habitsApi";
import type { Habit } from "../types/Habit";
import { Layout } from "../components/Layout";
import { HabitCard } from "../components/HabitCard";

export default function PublicHabitsPage() {
  const [habits, setHabits] = useState<Habit[]>([]);
  const [error, setError] = useState<string | null>(null);

  const loadPublic = useCallback(async () => {
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
      await loadPublic();
    })();
  }, [loadPublic]);

  return (
    <Layout>
      <h2>Публичные привычки</h2>
      <p style={{ marginBottom: 16, color: "#4b5563", fontSize: 14 }}>
        Это приятные и полезные привычки других пользователей. Вы можете использовать их как идеи и
        награды для своих полезных привычек.
      </p>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {habits.length === 0 ? (
        <p>Пока нет публичных привычек.</p>
      ) : (
        <div
          style={cardStyle}
        >
          {habits.map((h) => (
            <HabitCard key={h.id} habit={h} showActions={false} />
          ))}
        </div>
      )}
    </Layout>
  );
}

const cardStyle: React.CSSProperties = {
  background: "#fff",
  border: "1px solid #ddd",
  borderRadius: 10,
  padding: 16,
  display: "flex",
  flexDirection: "column",
  justifyContent: "space-between",
  minHeight: 240,
  boxShadow: "0 2px 6px rgba(0,0,0,0.06)",
  boxSizing: "border-box",
};
