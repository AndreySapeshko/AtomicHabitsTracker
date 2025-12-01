import { useEffect, useState } from "react";
import { habitsApi } from "../api/habitsApi";
import type { Habit, HabitCreateData } from "../types/Habit";
import { useNavigate } from "react-router-dom";

export default function HabitCreatePage() {
  const navigate = useNavigate();

  const [form, setForm] = useState<HabitCreateData>({
    action: "",
    place: "",
    time_of_day: "00:00",
    is_pleasant: false,
    related_pleasant_habit: null,
    reward_text: "",
    periodicity_days: 1,
    repeat_limit: 21,
    is_public: false,
  });

  const [pleasantHabits, setPleasantHabits] = useState<Habit[]>([]);
  const [error, setError] = useState<string | null>(null);

  async function loadPleasantHabits() {
    try {
      const res = await habitsApi.getPleasantHabits();
      setPleasantHabits(res.data);
    } catch (err) {
      console.error("Ошибка загрузки pleasant-привычек:", err);
    }
  }

  function update<K extends keyof HabitCreateData>(key: K, value: HabitCreateData[K]) {
    setForm((prev) => ({ ...prev, [key]: value }));
  }

  useEffect(() => {
    (async () => {
      await loadPleasantHabits();
    })();
  }, []);

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);

    // --- ВАЛИДАЦИЯ ПОД BACKEND-ЛОГИКУ ---

    if (form.is_pleasant) {
      // приятная привычка: НЕТ reward_text и НЕТ related_pleasant_habit
      if (form.related_pleasant_habit !== null) {
        setError("Приятная привычка не может иметь связанную привычку-награду.");
        return;
      }
      if (form.reward_text) {
        setError("Приятная привычка не может иметь текстовую награду.");
        return;
      }
    } else {
      // полезная привычка: либо reward_text, либо related_pleasant_habit (но не оба)
      const hasRelated = form.related_pleasant_habit !== null;
      const hasReward = !!form.reward_text?.trim();

      if (hasRelated === hasReward) {
        setError(
          "Для полезной привычки укажите либо приятную привычку-награду, либо текст награды (только одно).",
        );
        return;
      }
    }

    try {
      await habitsApi.createHabit(form);
      navigate("/habits");
    } catch (err) {
      console.error(err);
      setError("Ошибка сохранения привычки");
    }
  }

  const PERIODICITY = [1, 2, 3, 5, 7];
  const LIMITS = [21, 30, 45];

  return (
    <div style={{ padding: 20 }}>
      <h2>Создать привычку</h2>

      {error && <p style={{ color: "red" }}>{error}</p>}

      <form onSubmit={submit}>
        <label>Действие</label>
        <br />
        <input value={form.action} onChange={(e) => update("action", e.target.value)} required />
        <br />
        <br />

        <label>Место</label>
        <br />
        <input value={form.place} onChange={(e) => update("place", e.target.value)} required />
        <br />
        <br />

        <label>
          <input
            type="checkbox"
            checked={form.is_pleasant}
            onChange={(e) => update("is_pleasant", e.target.checked)}
          />
          Приятная привычка
        </label>

        <br />
        <br />

        {/* для приятной привычки пользователь видит только действие, место и публичность */}
        {/* время/периодичность/лимит мы можем либо скрыть, либо оставить общими */}
        {!form.is_pleasant && (
          <>
            <label>Время выполнения</label>
            <br />
            <input
              type="time"
              value={form.time_of_day}
              onChange={(e) => update("time_of_day", e.target.value)}
              required
            />
            <br />
            <br />

            <label>Периодичность (раз в X дней)</label>
            <br />
            <select
              value={form.periodicity_days}
              onChange={(e) => update("periodicity_days", Number(e.target.value))}
            >
              {PERIODICITY.map((d) => (
                <option key={d} value={d}>
                  {d} дней
                </option>
              ))}
            </select>

            <br />
            <br />

            <label>Лимит повторов</label>
            <br />
            <select
              value={form.repeat_limit}
              onChange={(e) => update("repeat_limit", Number(e.target.value))}
            >
              {LIMITS.map((l) => (
                <option key={l} value={l}>
                  {l} повторов
                </option>
              ))}
            </select>

            <br />
            <br />

            <label>Награда (текст)</label>
            <br />
            <input
              value={form.reward_text ?? ""}
              onChange={(e) => update("reward_text", e.target.value)}
            />
            <br />
            <br />

            <label>Приятная привычка-награда</label>
            <br />
            <select
              value={form.related_pleasant_habit ?? ""}
              onChange={(e) =>
                update("related_pleasant_habit", e.target.value ? Number(e.target.value) : null)
              }
            >
              <option value="">Не выбрано</option>
              {pleasantHabits.map((h) => (
                <option key={h.id} value={h.id}>
                  {h.action}
                </option>
              ))}
            </select>

            <br />
            <br />
          </>
        )}

        <label>
          <input
            type="checkbox"
            checked={form.is_public}
            onChange={(e) => update("is_public", e.target.checked)}
          />
          Публичная привычка
        </label>

        <br />
        <br />

        <button type="submit">Создать привычку</button>
      </form>
    </div>
  );
}
