import { useEffect, useState } from "react";
import { habitsApi } from "../api/habitsApi";
import type { Habit } from "../types/Habit";

export default function HabitsPage() {
  const [habits, setHabits] = useState<Habit[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadHabits();
  }, []);

  async function loadHabits() {
    try {
      const response = await habitsApi.getHabits();
      setHabits(response.data);
    } catch (err) {
      console.error(err);
      alert("Ошибка загрузки привычек");
    } finally {
      setLoading(false);
    }
  }

  if (loading) return <div>Загрузка...</div>;

  return (
    <div>
      <h2>Мои привычки</h2>

      {habits.length === 0 ? (
        <p>Нет привычек. Создайте первую!</p>
      ) : (
        <ul>
          {habits.map((h) => (
            <li key={h.id}>
              <strong>{h.action}</strong> – {h.time} ({h.place})
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
