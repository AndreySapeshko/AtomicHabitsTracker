import { useEffect, useState, useCallback } from "react";
import { useParams, Link } from "react-router-dom";
import { habitsApi } from "../api/habitsApi";
import type { Habit } from "../types/Habit";

interface HabitDetailsResponse {
  habit: Habit;
  progress: {
    completed: number;
    missed: number;
    pending: number;
    remaining: number;
    streak: number;
  };
  instances: {
    id: number;
    scheduled_datetime: string;
    status: string;
  }[];
}

export default function HabitDetailsPage() {
  const { id } = useParams();

  const [data, setData] = useState<HabitDetailsResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const loadDetails = useCallback(async () => {
    try {
      const res = await habitsApi.details(Number(id));
      setData(res.data);
    } catch (err) {
      console.error(err);
      setError("Ошибка загрузки данных привычки");
    }
  }, [id]);

  useEffect(() => {
    (async () => {
      await loadDetails();
    })();
  }, [loadDetails]);

  async function toggleActive() {
    if (!data) return;

    try {
      await habitsApi.updateHabit(data.habit.id, {
        is_active: !data.habit.is_active,
      });

      loadDetails(); // перегружаем после обновления
    } catch (err) {
      console.error(err);
      setError("Не удалось изменить статус активности");
    }
  }

  if (error) return <div style={{ padding: 20 }}>{error}</div>;
  if (!data) return <div style={{ padding: 20 }}>Загрузка...</div>;

  const habit = data.habit;
  const progress = data.progress;

  return (
    <div style={{ padding: 20 }}>
      <h2>Привычка: {habit.action}</h2>

      <p>
        <b>Место:</b> {habit.place}
      </p>
      <p>
        <b>Тип:</b> {habit.is_pleasant ? "Приятная" : "Полезная"}
      </p>
      <p>
        <b>Периодичность:</b> {habit.periodicity_days} дней
      </p>
      <p>
        <b>Лимит:</b> {habit.repeat_limit} повторов
      </p>
      <p>
        <b>Публичная:</b> {habit.is_public ? "Да" : "Нет"}
      </p>
      <p>
        <b>Активность:</b> {habit.is_active ? "Активна" : "Неактивна"}
      </p>

      {!habit.is_pleasant && (
        <>
          <p>
            <b>Время дня:</b> {habit.time_of_day}
          </p>

          {habit.reward_text && (
            <p>
              <b>Награда:</b> {habit.reward_text}
            </p>
          )}
          {habit.related_pleasant_habit && (
            <p>
              <b>Награда:</b> Приятная привычка #{habit.related_pleasant_habit}
            </p>
          )}
        </>
      )}

      <br />

      <h3>Прогресс</h3>
      <p>✔ Выполнено: {progress.completed}</p>
      <p>❌ Пропущено: {progress.missed}</p>
      <p>⏳ В ожидании: {progress.pending}</p>
      <p>🔥 Streak: {progress.streak}</p>
      <p>🎯 Осталось до цели: {progress.remaining}</p>

      <br />

      <h3>Последние инстансы</h3>
      <ul>
        {data.instances.map((inst) => (
          <li key={inst.id}>
            {inst.scheduled_datetime} — {inst.status}
          </li>
        ))}
      </ul>

      <br />

      <button onClick={toggleActive}>
        {habit.is_active ? "🔴 Деактивировать" : "🟢 Активировать снова"}
      </button>

      <br />
      <br />

      <Link to={`/habits/${habit.id}/edit`}>
        <button>✏ Редактировать</button>
      </Link>

      <br />
      <br />

      <Link to="/habits">
        <button>← Назад к списку</button>
      </Link>
    </div>
  );
}
