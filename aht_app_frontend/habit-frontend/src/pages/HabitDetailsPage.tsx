import { useEffect, useState, useCallback } from "react";
import { useParams, Link } from "react-router-dom";
import { habitsApi } from "../api/habitsApi";
import type { Habit } from "../types/Habit";
import type { HabitStats } from "../types/HabitStats";
import { ProgressBar } from "../components/ProgressBar";
import { CompletionPieChart } from "../components/CompletionPieChart";
import { WeeklyBarChart } from "../components/WeeklyBarChart";

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
  const [stats, setStats] = useState<HabitStats | null>(null);

  const loadStats = useCallback(async () => {
    try {
      const res = await habitsApi.stats(Number(id));
      setStats(res.data);
    } catch (err) {
      console.error(err);
    }
  }, [id]);

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
      await loadStats();
    })();
  }, [loadDetails, loadStats]);

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
  if (!stats) {
    return <div style={{ padding: 20 }}>Загрузка статистики...</div>;
  }

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

      <br />
      <h3>Статистика</h3>

      {stats ? (
        <div style={{ paddingLeft: 10 }}>
          <p>
            <b>🔥 Текущий стрик:</b> {stats.current_streak}
          </p>
          <p>
            <b>🏆 Максимальный стрик:</b> {stats.max_streak}
          </p>

          {!habit.is_pleasant && (
            <>
              <p>
                <b>🎯 Лимит:</b> {stats.repeat_limit}
              </p>
              <p>
                <b>📊 Прогресс (%):</b> {stats.progress_percent}%
              </p>
            </>
          )}

          <p>
            <b>✔ Всего выполнено:</b> {stats.total_completed}
          </p>
          <p>
            <b>❌ Всего пропущено:</b> {stats.total_missed}
          </p>
          <p>
            <b>⏳ В ожидании:</b> {stats.total_pending}
          </p>

          <br />

          <h4>Последние 30 дней</h4>
          <ul>
            {Object.entries(stats.last_30_days).map(([date, status]) => (
              <li key={date}>
                {date}: {status}
              </li>
            ))}
          </ul>

          <h4>По неделям</h4>
          <ul>
            {stats.per_week.map((w) => (
              <li key={w.week}>
                {w.week}: ✔ {w.completed}, ❌ {w.missed}
              </li>
            ))}
          </ul>
        </div>
      ) : (
        <p>Загрузка статистики...</p>
      )}

      <h3>📊 Визуальная статистика</h3>

      {/* Прогресс бар */}
      {stats.progress_percent !== null && (
        <>
          <h4>Прогресс к цели</h4>
          <ProgressBar percent={stats.progress_percent} />
        </>
      )}

      {/* Streak UI */}
      <div style={{ marginTop: 20, padding: 10, border: "1px solid #ccc", borderRadius: 8 }}>
        <h4>🔥 Streak</h4>
        <p>
          Текущий: <b>{stats.current_streak}</b>
        </p>
        <p>
          Максимальный: <b>{stats.max_streak}</b>
        </p>
      </div>

      {/* Pie chart */}
      <div style={{ marginTop: 20 }}>
        <h4>Соотношение выполнено/пропущено</h4>
        <CompletionPieChart
          completed={stats.total_completed}
          missed={stats.total_missed}
          pending={stats.total_pending}
        />
      </div>

      {/* Weekly bars */}
      <div style={{ marginTop: 20 }}>
        <h4>Статистика по неделям</h4>
        <WeeklyBarChart data={stats.per_week} />
      </div>

      <div style={{ marginTop: 20, padding: 10, border: "1px solid #ddd", borderRadius: 8 }}>
        <h3>🔥 Streak</h3>
        <p>
          <b>Текущий стрик:</b> {stats.current_streak} дней
        </p>
        <p>
          <b>Максимальный стрик:</b> {stats.max_streak} дней
        </p>
      </div>

      <h3>Последние инстансы</h3>
      <ul>
        {data.instances.map((inst) => (
          <li key={inst.id}>
            {inst.scheduled_datetime} — {inst.status}
          </li>
        ))}
      </ul>

      <Link to={`/habits/${habit.id}/instances`}>
        <button>📋 История выполнения</button>
      </Link>

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
