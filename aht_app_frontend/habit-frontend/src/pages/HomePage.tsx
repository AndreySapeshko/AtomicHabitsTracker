import { useEffect, useState } from "react";
import { habitsApi } from "../api/habitsApi";
import type { Habit } from "../types/Habit";
import type { HabitInstance } from "../types/HabitInstance";
import { Link } from "react-router-dom";

export default function HomePage() {
  const [today, setToday] = useState<HabitInstance[]>([]);
  const [habits, setHabits] = useState<Habit[]>([]);

  useEffect(() => {
    (async () => {
      try {
        const h = await habitsApi.getHabits();
        setHabits(h.data);

        const inst = await habitsApi.instancesForToday();
        setToday(inst.data);
      } catch (err) {
        console.error(err);
      }
    })();
  }, []);

  return (
    <div style={{ padding: 20 }}>
      <h2>Добро пожаловать 👋</h2>

      <h3>Ваши привычки</h3>
      <p>
        Активных привычек: <b>{habits.filter((h) => h.is_active).length}</b>
      </p>

      <Link to="/habits/new">
        <button>➕ Создать новую привычку</button>
      </Link>

      <hr />

      <h3>Сегодняшние задачи</h3>
      {today.length === 0 ? (
        <p>Сегодня нет задач 🎉</p>
      ) : (
        <ul>
          {today.map((inst) => (
            <li key={inst.id}>
              <Link to={`/habits/${inst.habit}`}>
                {inst.time} — {inst.action}
              </Link>
            </li>
          ))}
        </ul>
      )}

      <hr />

      <h3>Быстрые ссылки</h3>
      <ul>
        <li><Link to="/habits">Все привычки</Link></li>
        <li><Link to="/habits/public">Публичные привычки</Link></li>
      </ul>
    </div>
  );
}
