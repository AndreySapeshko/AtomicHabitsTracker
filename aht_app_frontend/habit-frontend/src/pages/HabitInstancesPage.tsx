import { useEffect, useState, useCallback } from "react";
import { useParams, Link } from "react-router-dom";
import { habitsApi } from "../api/habitsApi";
import { formatDateTime } from "../utils/formatDate";

interface HabitInstance {
  id: number;
  scheduled_datetime: string;
  confirm_deadline: string;
  status: string;
}

export default function HabitInstancesPage() {
  const { id } = useParams();
  const habitId = Number(id);

  const [instances, setInstances] = useState<HabitInstance[]>([]);
  const [statusFilter, setStatusFilter] = useState<string>("");

  const loadInstances = useCallback(async () => {
  try {
    const response = await habitsApi.instances(habitId, { status: statusFilter || undefined });
    setInstances(response.data);
  } catch (err) {
    console.error(err);
  }
}, [habitId, statusFilter]);
  
  useEffect(() => {
    (async () => {
      await loadInstances()
    })();
    ;
  }, [loadInstances]);

  return (
    <div style={{ padding: 20 }}>
      <h2>История выполнения привычки #{habitId}</h2>

      <div style={{ marginBottom: 15 }}>
        <label>Фильтр по статусу: </label>
        <select
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value)}
        >
          <option value="">Все</option>
          <option value="scheduled">Запланировано</option>
          <option value="pending">Ожидает выполнения</option>
          <option value="completed">Выполнено</option>
          <option value="completed_late">Выполнено с опозданием</option>
          <option value="missed">Пропущено</option>
          <option value="fix_expired">Просрочено</option>
        </select>
      </div>

      <table border={1} cellPadding={8}>
        <thead>
          <tr>
            <th>Запланировано</th>
            <th>Дедлайн</th>
            <th>Статус</th>
          </tr>
        </thead>

        <tbody>
          {instances.map((inst) => (
            <tr key={inst.id}>
              <td>{formatDateTime(inst.scheduled_datetime)}</td>
              <td>{formatDateTime(inst.confirm_deadline)}</td>
              <td>{inst.status}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <br />

      <Link to={`/habits/${habitId}`}>
        <button>← Назад к детали</button>
      </Link>
    </div>
  );
}
