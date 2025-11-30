import { useEffect, useState } from "react";
import { habitsApi } from "../api/habitsApi";
import type { Habit } from "../types/Habit";
import { Link } from "react-router-dom";

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

      <Link to="/habits/create">
        <button>Создать привычку</button>
      </Link>

      <br />
      <br />

      {habits.length === 0 ? (
        <p>Нет привычек. Создайте первую!</p>
      ) : (
        <ul>
          {habits.map((h) => (
            <li key={h.id}>
              <strong>{h.action}</strong> – {h.time_of_day} ({h.place})
              <Link to={`/habits/${h.id}/edit`}>
                <button>Редактировать</button>
              </Link>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
