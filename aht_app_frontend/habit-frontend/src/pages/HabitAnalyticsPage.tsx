import { useEffect, useState, useCallback } from "react";
import { useParams, Link } from "react-router-dom";
import { habitsApi } from "../api/habitsApi";
import type { HabitStats } from "../types/HabitStats";
import { ProgressBar } from "../components/ProgressBar";
import { CompletionPieChart } from "../components/CompletionPieChart";
import { WeeklyBarChart } from "../components/WeeklyBarChart";
import { Layout } from "../components/Layout";

export default function HabitAnalyticsPage() {
  const { id } = useParams();
  const habitId = Number(id);

  const [stats, setStats] = useState<HabitStats | null>(null);
  const [habitName, setHabitName] = useState("");

  const loadStats = useCallback(async () => {
    const response = await habitsApi.stats(habitId);
    setStats(response.data);
  }, [habitId]);

  const loadHabit = useCallback(async () => {
    const response = await habitsApi.details(habitId);
    setHabitName(response.data.habit.action);
  }, [habitId]);

  useEffect(() => {
    (async () => {
      await loadHabit();
      await loadStats();
    })();
  }, [loadHabit, loadStats]);

  if (!stats) return <div style={{ padding: 20 }}>Загрузка...</div>;

  return (
    <Layout>
      <div style={{ padding: 20 }}>
        <h2>📊 Аналитика привычки</h2>
        <h3 style={{ marginBottom: 30 }}>“{habitName}”</h3>

        {/* Навигация */}
        <div style={{ display: "flex", gap: 10, marginBottom: 20 }}>
          <Link to={`/habits/${habitId}`}>← Назад к привычке</Link>
          <Link to={`/habits/${habitId}/instances`}>История выполнения</Link>
          <Link to={`/habits/${habitId}/edit`}>Редактировать</Link>
        </div>

        <section style={{ marginBottom: 40 }}>
          <h3>🎯 Прогресс</h3>
          <ProgressBar percent={stats.progress_percent ?? 0} />
          <p>Осталось повторов: {stats.repeat_limit}</p>
        </section>

        <section style={{ marginBottom: 40 }}>
          <h3>🔥 Streak</h3>
          <p>
            <b>Текущий стрик:</b> {stats.current_streak}
          </p>
          <p>
            <b>Максимальный стрик:</b> {stats.max_streak}
          </p>
        </section>

        <section style={{ marginBottom: 40 }}>
          <h3>🥧 Выполнено / Пропущено</h3>
          <CompletionPieChart
            completed={stats.total_completed}
            missed={stats.total_missed}
            pending={stats.total_pending}
          />
        </section>

        <section style={{ marginBottom: 40 }}>
          <h3>📅 Выполнения по неделям</h3>
          <WeeklyBarChart data={stats.per_week} />
        </section>

        <section style={{ marginBottom: 40 }}>
          <h3>🗓 Последние 30 дней</h3>
          <table style={{ borderCollapse: "collapse", marginTop: 10 }}>
            <thead>
              <tr>
                <th style={{ padding: 5, borderBottom: "1px solid #ddd" }}>Дата</th>
                <th style={{ padding: 5, borderBottom: "1px solid #ddd" }}>Статус</th>
              </tr>
            </thead>

            <tbody>
              {Object.entries(stats.last_30_days).map(([date, status]) => (
                <tr key={date}>
                  <td style={{ padding: 5 }}>{date}</td>
                  <td style={{ padding: 5 }}>{status}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>
      </div>
    </Layout>
  );
}
