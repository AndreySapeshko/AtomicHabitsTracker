interface ProgressBarProps {
  percent: number;
}

export function ProgressBar({ percent }: ProgressBarProps) {
  return (
    <div style={{ width: "100%", background: "#eee", borderRadius: 6, height: 20 }}>
      <div
        style={{
          width: `${percent}%`,
          background: percent >= 100 ? "#4caf50" : "#2196f3",
          height: "100%",
          borderRadius: 6,
          transition: "0.3s",
          textAlign: "center",
          color: "white",
          fontSize: 12,
        }}
      >
        {percent}%
      </div>
    </div>
  );
}
