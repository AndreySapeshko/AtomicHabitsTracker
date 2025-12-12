import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from "recharts";
import type { HabitWeekStat } from "../types/HabitStats";

export function WeeklyBarChart({ data }: { data: HabitWeekStat[] }) {
  return (
    <BarChart width={500} height={300} data={data}>
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="week" />
      <YAxis />
      <Tooltip />
      <Legend />

      <Bar dataKey="completed" fill="#4caf50" name="Выполнено" />
      <Bar dataKey="missed" fill="#f44336" name="Пропущено" />
    </BarChart>
  );
}
