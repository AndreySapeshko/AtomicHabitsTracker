import { useEffect, useState, useCallback } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { habitsApi } from "../api/habitsApi";
import type { Habit, HabitCreateData } from "../types/Habit";

export default function HabitEditPage() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [habit, setHabit] = useState<Habit | null>(null);
  const [form, setForm] = useState<HabitCreateData | null>(null);
  const [error, setError] = useState<string | null>(null);

  const [pleasantHabits, setPleasantHabits] = useState<Habit[]>([]);

  function update<K extends keyof HabitCreateData>(key: K, value: HabitCreateData[K]) {
    if (!form) return;
    setForm({ ...form, [key]: value });
  }

  const loadHabit = useCallback(async () => {
  try {
    const res = await habitsApi.getHabit(Number(id));
    const data = res.data;

    setHabit(data);

    setForm({
      action: data.action,
      place: data.place,
      time_of_day: data.time_of_day ?? "00:00",
      is_pleasant: data.is_pleasant,
      related_pleasant_habit: data.related_pleasant_habit,
      reward_text: data.reward_text,
      periodicity_days: data.periodicity_days,
      repeat_limit: data.repeat_limit,
      is_public: data.is_public,
      is_active: data.is_active,
    });
  } catch (err) {
    console.error(err);
  }
}, [id]);  // зависимость ОДНА — id


const loadPleasantHabits = useCallback(async () => {
  try {
    const res = await habitsApi.getPleasantHabits();
    setPleasantHabits(res.data);
  } catch (err) {
    console.error(err);
  }
}, []);  // нет зависимостей


useEffect(() => {
  (async () => {
    await loadHabit();  
    await loadPleasantHabits();
    })();
}, [loadHabit, loadPleasantHabits]);


  async function submit(e: React.FormEvent) {
    e.preventDefault();
    if (!form) return;

    setError(null);

    // Валидация pleasant / полезная
    if (form.is_pleasant) {
      if (form.related_pleasant_habit !== null) {
        setError("Приятная привычка не может иметь наградную привычку.");
        return;
      }
      if (form.reward_text) {
        setError("Приятная привычка не может иметь текстовую награду.");
        return;
      }
    } else {
      const hasReward = !!form.reward_text?.trim();
      const hasRelated = form.related_pleasant_habit !== null;

      if (hasReward === hasRelated) {
        setError(
          "Полезная привычка должна иметь либо текст награды, либо pleasant habit — но не оба.",
        );
        return;
      }
    }

    try {
      await habitsApi.updateHabit(Number(id), form);
      navigate("/habits");
    } catch (err) {
      console.error(err);
      setError("Ошибка сохранения изменений");
    }
  }

  async function toggleActive() {
    if (!habit) return;

    try {
      await habitsApi.updateHabit(habit.id, { is_active: !habit.is_active });
      loadHabit(); // перезагрузим данные
    } catch (err) {
      console.error(err);
    }
  }

  if (!form || !habit) return <div>Загрузка...</div>;

  const PERIODICITY = [1, 2, 3, 5, 7];
  const LIMITS = [21, 30, 45];

  return (
    <div style={{ padding: 20 }}>
      <h2>Редактировать привычку</h2>

      {error && <p style={{ color: "red" }}>{error}</p>}

      <button onClick={toggleActive}>
        {habit.is_active ? "🔴 Деактивировать" : "🟢 Активировать заново"}
      </button>

      <br />
      <br />

      <form onSubmit={submit}>
        <label>Действие</label>
        <br />
        <input value={form.action} onChange={(e) => update("action", e.target.value)} />
        <br />
        <br />

        <label>Место</label>
        <br />
        <input value={form.place} onChange={(e) => update("place", e.target.value)} />
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

        {!form.is_pleasant && (
          <>
            <label>Время выполнения</label>
            <br />
            <input
              type="time"
              value={form.time_of_day}
              onChange={(e) => update("time_of_day", e.target.value)}
            />
            <br />
            <br />

            <label>Периодичность</label>
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
              {LIMITS.map((d) => (
                <option key={d} value={d}>
                  {d} повторов
                </option>
              ))}
            </select>
            <br />
            <br />

            <label>Текст награды</label>
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

        <button type="submit">Сохранить изменения</button>
      </form>
    </div>
  );
}
