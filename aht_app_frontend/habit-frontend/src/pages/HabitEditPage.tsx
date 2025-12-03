import { useEffect, useState, useCallback } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { habitsApi } from "../api/habitsApi";
import type { Habit } from "../types/Habit";
import type { HabitCreateData } from "../types/Habit";

export default function HabitEditPage() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [habit, setHabit] = useState<Habit | null>(null);
  const [form, setForm] = useState<HabitCreateData | null>(null);
  const [pleasantList, setPleasantList] = useState<Habit[]>([]);
  const [rewardMode, setRewardMode] = useState<"text" | "pleasant" | null>(null);

  const [error, setError] = useState<string | null>(null);

  // Загружаем привычку
  const loadHabit = useCallback(async () => {
    try {
      const res = await habitsApi.details(Number(id));
      const h: Habit = res.data.habit;

      setHabit(h);

      // Заполняем форму начальными значениями
      setForm({
        action: h.action,
        place: h.place,
        time_of_day: h.time_of_day,
        is_pleasant: h.is_pleasant,
        periodicity_days: h.periodicity_days,
        repeat_limit: h.repeat_limit,
        reward_text: h.reward_text,
        related_pleasant_habit: h.related_pleasant_habit,
        is_public: h.is_public,
      });

      // Определяем rewardMode
      if (h.reward_text) setRewardMode("text");
      else if (h.related_pleasant_habit) setRewardMode("pleasant");
      else setRewardMode(null);
    } catch (err) {
      console.error(err);
      setError("Ошибка загрузки привычки");
    }
  }, [id]);

  // Загружаем приятные привычки для списка наград
  const loadPleasant = useCallback(async () => {
    try {
      const res = await habitsApi.pleasant();
      setPleasantList(res.data);
    } catch (err) {
      console.error(err);
    }
  }, []);

  useEffect(() => {
    (async () => {
      await loadHabit();
      await loadPleasant();
    })();
  }, [loadHabit, loadPleasant]);

  // Утилита обновления полей
  const update = <K extends keyof HabitCreateData>(field: K, value: HabitCreateData[K]) => {
    setForm((prev) => (prev ? { ...prev, [field]: value } : prev));
  };

  // Сохранение
  async function submit(e: React.FormEvent) {
    e.preventDefault();
    if (!form || !habit) return;

    const payload = {
      ...form,
      reward_text: rewardMode === "text" ? form.reward_text : null,
      related_pleasant_habit: rewardMode === "pleasant" ? form.related_pleasant_habit : null,
    };

    try {
      await habitsApi.updateHabit(habit.id, payload);
      navigate(`/habits/${habit.id}`);
    } catch (err) {
      console.error(err);
      setError("Ошибка сохранения изменений");
    }
  }

  if (!habit || !form) return <div style={{ padding: 20 }}>Загрузка...</div>;
  if (error) return <div style={{ padding: 20, color: "red" }}>{error}</div>;

  const isPleasantHabit = habit.is_pleasant;

  return (
    <div style={{ padding: 20, maxWidth: 800, margin: "0 auto" }}>
      <h2>Редактирование привычки</h2>

      <form onSubmit={submit}>
        {/* Тип (нельзя менять!) */}
        <p>
          <b>Тип:</b> {habit.is_pleasant ? "Приятная" : "Полезная"} (тип изменить нельзя)
        </p>

        {/* Действие */}
        <label>
          Действие:
          <input
            type="text"
            value={form.action}
            onChange={(e) => update("action", e.target.value)}
          />
        </label>
        <br />

        {/* Место */}
        <label>
          Место:
          <input type="text" value={form.place} onChange={(e) => update("place", e.target.value)} />
        </label>
        <br />

        {/* Публичность */}
        <label>
          <input
            type="checkbox"
            checked={form.is_public}
            onChange={(e) => update("is_public", e.target.checked)}
          />{" "}
          Публичная
        </label>

        <br />
        <hr />
        <br />

        {!isPleasantHabit && (
          <>
            {/* Время */}
            <label>
              Время выполнения:
              <input
                type="time"
                value={form.time_of_day}
                onChange={(e) => update("time_of_day", e.target.value)}
              />
            </label>
            <br />

            {/* Периодичность */}
            <label>
              Периодичность:
              <select
                value={form.periodicity_days}
                onChange={(e) => update("periodicity_days", Number(e.target.value))}
              >
                <option value={1}>Каждый день</option>
                <option value={2}>Раз в 2 дня</option>
                <option value={3}>Раз в 3 дня</option>
                <option value={5}>Раз в 5 дней</option>
                <option value={7}>Раз в неделю</option>
              </select>
            </label>
            <br />

            {/* Лимит */}
            <label>
              Лимит повторов:
              <select
                value={form.repeat_limit}
                onChange={(e) => update("repeat_limit", Number(e.target.value))}
              >
                <option value={21}>21 повтор</option>
                <option value={30}>30 повторов</option>
                <option value={45}>45 повторов</option>
              </select>
            </label>

            <br />
            <br />

            {/* Награда */}
            <b>Награда</b>
            <div style={{ marginTop: 8 }}>
              <label>
                <input
                  type="radio"
                  checked={rewardMode === "text"}
                  onChange={() => {
                    setRewardMode("text");
                    update("related_pleasant_habit", null);
                  }}
                />
                Текстовая награда
              </label>

              <label style={{ marginLeft: 20 }}>
                <input
                  type="radio"
                  checked={rewardMode === "pleasant"}
                  onChange={() => {
                    setRewardMode("pleasant");
                    update("reward_text", "");
                  }}
                />
                Приятная привычка
              </label>
            </div>

            {/* Текстовая награда */}
            {rewardMode === "text" && (
              <div style={{ marginTop: 10 }}>
                <input
                  type="text"
                  value={form.reward_text ?? ""}
                  onChange={(e) => update("reward_text", e.target.value)}
                />
              </div>
            )}

            {/* Приятная привычка */}
            {rewardMode === "pleasant" && (
              <div style={{ marginTop: 10 }}>
                <select
                  value={form.related_pleasant_habit ?? ""}
                  onChange={(e) => update("related_pleasant_habit", Number(e.target.value))}
                >
                  <option value="">Выберите привычку</option>
                  {pleasantList.map((p) => (
                    <option key={p.id} value={p.id}>
                      {p.action}
                    </option>
                  ))}
                </select>

                {pleasantList.length === 0 && (
                  <p style={{ color: "red" }}>
                    У вас нет приятных привычек. Создайте хотя бы одну.
                  </p>
                )}
              </div>
            )}
          </>
        )}

        <br />
        <br />
        <button type="submit">💾 Сохранить изменения</button>

        <br />
        <br />

        <button
          type="button"
          onClick={() =>
            habitsApi
              .updateHabit(habit.id, {
                is_active: !habit.is_active,
              })
              .then(() => loadHabit())
          }
        >
          {habit.is_active ? "🔴 Деактивировать" : "🟢 Активировать"}
        </button>

        <br />
        <br />

        <button type="button" onClick={() => navigate(`/habits/${habit.id}`)}>
          ← Назад
        </button>
      </form>
    </div>
  );
}
