import { useEffect, useState, useCallback } from "react";
import { habitsApi } from "../api/habitsApi";
import type { Habit } from "../types/Habit";
import { Layout } from "../components/Layout";
import { Button } from "../components/Button";
import { HabitCard } from "../components/HabitCard";
import { Link } from "react-router-dom";

export default function HabitsPage() {
  const [habits, setHabits] = useState<Habit[]>([]);
  const [error, setError] = useState<string | null>(null);

  const loadHabits = useCallback(async () => {
    try {
      const res = await habitsApi.getHabits();
      setHabits(res.data);
    } catch (err) {
      console.error(err);
      setError("Не удалось загрузить привычки");
    }
  }, []);

  useEffect(() => {
    (async () => {
      await loadHabits();
    })();
  }, [loadHabits]);

  return (
    <Layout>
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: 16,
        }}
      >
        <h2 style={{ margin: 0 }}>Мои привычки</h2>
        <Link to="/habits/create">
          <Button>➕ Новая привычка</Button>
        </Link>
      </div>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {habits.length === 0 ? (
        <p>У вас пока нет привычек. Создайте первую!</p>
      ) : (
        <div
          style={cardStyle}
        >
          {habits.map((h) => (
            <HabitCard key={h.id} habit={h} showActions/>
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
