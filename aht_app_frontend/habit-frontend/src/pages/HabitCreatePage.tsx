import { useState, useEffect, useCallback } from "react";
import { habitsApi } from "../api/habitsApi";
import { useNavigate } from "react-router-dom";
import type { Habit } from "../types/Habit";
import type { HabitCreateData } from "../types/Habit";
import { Layout } from "../components/Layout";

export default function HabitCreatePage() {
  const navigate = useNavigate();

  const [isPleasant, setIsPleasant] = useState(false);

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

  const [pleasantList, setPleasantList] = useState<Habit[]>([]);
  const [rewardMode, setRewardMode] = useState<"text" | "pleasant" | null>(null);

  const [error, setError] = useState<string | null>(null);

  const loadPleasant = useCallback(async () => {
    try {
      const res = await habitsApi.pleasant();
      setPleasantList(res.data);
    } catch (err) {
      console.error(err);
    }
  }, []);

  useEffect(() => {
    if (!isPleasant) {
      (async () => {
        await loadPleasant();
      })();
    }
  }, [isPleasant, loadPleasant]);

  const update = <K extends keyof HabitCreateData>(field: K, value: HabitCreateData[K]) => {
    setForm((prev) => ({
      ...prev,
      [field]: value,
    }));
  };

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);

    try {
      await habitsApi.createHabit(form);
      navigate("/habits");
    } catch (err) {
      console.error(err);
      setError("Ошибка создания привычки");
    }
  }

  return (
    <Layout>
      <div style={{ padding: 20, maxWidth: 800, margin: "0 auto" }}>
        <h2>Создание привычки</h2>

        <form onSubmit={submit}>
          {/* Тип */}
          <label>
            Тип привычки:
            <div style={{ marginTop: 8 }}>
              <label>
                <input
                  type="radio"
                  checked={isPleasant}
                  onChange={() => {
                    setIsPleasant(true);
                    update("is_pleasant", true);
                    update("reward_text", "");
                    update("related_pleasant_habit", null);
                  }}
                />{" "}
                Приятная
              </label>
              <label style={{ marginLeft: 20 }}>
                <input
                  type="radio"
                  checked={!isPleasant}
                  onChange={() => {
                    setIsPleasant(false);
                    update("is_pleasant", false);
                  }}
                />{" "}
                Полезная
              </label>
            </div>
          </label>

          <br />

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
            <input
              type="text"
              value={form.place}
              onChange={(e) => update("place", e.target.value)}
            />
          </label>
          <br />

          {/* Общий "публичность" */}
          <label>
            <input
              type="checkbox"
              checked={form.is_public}
              onChange={(e) => update("is_public", e.target.checked)}
            />{" "}
            Публичная привычка
          </label>

          <br />
          <hr />
          <br />

          {/* Если ПРИЯТНАЯ — остальные поля скрываем */}
          {isPleasant ? (
            <p style={{ color: "#555" }}>
              Приятная привычка создаётся без награды, времени и периодичности. Эти привычки
              используются как награды для полезных привычек.
            </p>
          ) : (
            <>
              {/* Полезная привычка — время */}
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

              {/* Выбор награды */}
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
                    placeholder="Введите награду"
                    value={form.reward_text ?? ""}
                    onChange={(e) => update("reward_text", e.target.value)}
                  />
                </div>
              )}

              {/* Приятная привычка как награда */}
              {rewardMode === "pleasant" && (
                <div style={{ marginTop: 10 }}>
                  {pleasantList.length === 0 ? (
                    <p style={{ color: "red" }}>
                      У вас нет приятных привычек — создайте хотя бы одну.
                    </p>
                  ) : (
                    <select
                      value={form.related_pleasant_habit ?? ""}
                      onChange={(e) => update("related_pleasant_habit", Number(e.target.value))}
                    >
                      <option value={""}>Выберите привычку</option>
                      {pleasantList.map((p) => (
                        <option key={p.id} value={p.id}>
                          {p.action}
                        </option>
                      ))}
                    </select>
                  )}
                </div>
              )}
            </>
          )}

          <br />
          <button type="submit">Создать</button>
        </form>

        {error && <p style={{ color: "red" }}>{error}</p>}
      </div>
    </Layout>
  );
}
