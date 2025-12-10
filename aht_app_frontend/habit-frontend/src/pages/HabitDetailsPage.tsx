import { useEffect, useState, useCallback } from "react";
import { useParams, Link, useNavigate } from "react-router-dom";
import { habitsApi } from "../api/habitsApi";
import type { Habit } from "../types/Habit";
import type { HabitStats } from "../types/HabitStats";
import { Card } from "../components/Card";
import { Layout } from "../components/Layout";

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
  const navigate = useNavigate();

  const [data, setData] = useState<HabitDetailsResponse | null>(null);
  const [stats, setStats] = useState<HabitStats | null>(null);
  const [error, setError] = useState<string | null>(null);

  const habitId = Number(id);

  const loadDetails = useCallback(async () => {
    try {
      const res = await habitsApi.details(habitId);
      setData(res.data);
    } catch {
      setError("Ошибка загрузки данных привычки");
    }
  }, [habitId]);

  const loadStats = useCallback(async () => {
    try {
      const res = await habitsApi.stats(habitId);
      setStats(res.data);
    } catch {
      console.error("Ошибка загрузки статистики");
    }
  }, [habitId]);

  const handleDelete = async () => {
    if (!confirm("Удалить привычку?")) return;

    await habitsApi.deleteHabit(habit.id);
    navigate("/habits");
  };

  useEffect(() => {
    (async () => {
      await loadDetails();
      await loadStats();
    })();
  }, [loadDetails, loadStats]);

  async function toggleActive() {
    if (!data) return;
    try {
      await habitsApi.updateHabit(data.habit.id, {
        is_active: !data.habit.is_active,
      });
      loadDetails();
    } catch {
      setError("Не удалось изменить статус активности");
    }
  }

  if (error) return <div style={{ padding: 20 }}>{error}</div>;
  if (!data || !stats) return <div style={{ padding: 20 }}>Загрузка...</div>;

  const habit = data.habit;
  const progress = data.progress;

  return (
    <Layout>
      <div style={{ padding: 20, maxWidth: 800 }}>
        <h2 style={{ marginBottom: 20 }}>Привычка: {habit.action}</h2>

        {/* Основная информация */}
        <Card>
          <h3>ℹ Информация</h3>
          <p>
            <b>Место:</b> {habit.place}
          </p>
          <p>
            <b>Тип:</b> {habit.is_pleasant ? "Приятная" : "Полезная"}
          </p>
          <p>
            <b>Периодичность:</b> каждые {habit.periodicity_days} дня
          </p>
          <p>
            <b>Лимит:</b> {habit.repeat_limit} повторов
          </p>
          <p>
            <b>Публичная:</b> {habit.is_public ? "Да" : "Нет"}
          </p>
          <p>
            <b>Статус:</b> {habit.is_active ? "Активна" : "Неактивна"}
          </p>
        </Card>

        {/* Награда */}
        {!habit.is_pleasant && (
          <Card>
            <h3>🎁 Награда</h3>
            <p>
              <b>Время:</b> {habit.time_of_day}
            </p>

            {habit.reward_text && (
              <p>
                <b>Награда:</b> {habit.reward_text}
              </p>
            )}

            {habit.related_pleasant_habit && (
              <p>
                <b>Наградная привычка:</b> Приятная #{habit.related_pleasant_habit}
              </p>
            )}
          </Card>
        )}

        {/* Прогресс */}
        <Card>
          <h3>📈 Прогресс</h3>
          <p>✔ Выполнено: {progress.completed}</p>
          <p>❌ Пропущено: {progress.missed}</p>
          <p>⏳ В ожидании: {progress.pending}</p>
          <p>🔥 Streak: {progress.streak}</p>
          <p>🎯 Осталось повторов: {progress.remaining}</p>
        </Card>

        {/* Последние инстансы */}
        <Card>
          <h3>🕒 Последние 20 выполнений</h3>
          <ul>
            {data.instances.map((inst) => (
              <li key={inst.id}>
                {inst.scheduled_datetime} — {inst.status}
              </li>
            ))}
          </ul>
        </Card>

        {/* Кнопки */}
        <div style={{ display: "flex", gap: 10, marginTop: 20 }}>
          <Link to={`/habits/${habit.id}/instances`}>
            <button>📋 История</button>
          </Link>

          <Link to={`/habits/${habit.id}/analytics`}>
            <button>📊 Аналитика</button>
          </Link>

          <Link to={`/habits/${habit.id}/edit`}>
            <button>✏ Редактировать</button>
          </Link>

          <button onClick={handleDelete} className="danger">
            Удалить
          </button>

          <button onClick={toggleActive}>
            {habit.is_active ? "🔴 Остановить" : "🟢 Запустить снова"}
          </button>
        </div>

        <br />

        <Link to="/habits">← Назад к списку</Link>
      </div>
    </Layout>
  );
}
