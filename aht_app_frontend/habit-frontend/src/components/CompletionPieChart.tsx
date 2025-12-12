import { PieChart, Pie, Cell, Tooltip, Legend } from "recharts";

interface Props {
  completed: number;
  missed: number;
  pending: number;
}

const COLORS = {
  completed: "#4caf50",
  missed: "#f44336",
  pending: "#ff9800",
};

export function CompletionPieChart({ completed, missed, pending }: Props) {
  const data = [
    { name: "Выполнено", value: completed, color: COLORS.completed },
    { name: "Пропущено", value: missed, color: COLORS.missed },
    { name: "Ожидает", value: pending, color: COLORS.pending },
  ];

  return (
    <PieChart width={300} height={250}>
      <Pie
        data={data}
        cx={150}
        cy={120}
        innerRadius={40}
        outerRadius={80}
        paddingAngle={2}
        dataKey="value"
      >
        {data.map((entry, idx) => (
          <Cell key={idx} fill={entry.color} />
        ))}
      </Pie>
      <Tooltip />
      <Legend />
    </PieChart>
  );
}
