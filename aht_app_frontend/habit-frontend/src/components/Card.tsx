export function Card({ children }: { children: React.ReactNode }) {
  return (
    <div
      style={{
        padding: 16,
        border: "1px solid #ddd",
        borderRadius: 8,
        marginBottom: 20,
        background: "#fff",
      }}
    >
      {children}
    </div>
  );
}
