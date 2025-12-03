import type { ButtonHTMLAttributes } from "react";

type Variant = "primary" | "secondary" | "danger" | "ghost";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: Variant;
}

export function Button({ variant = "primary", style, ...props }: ButtonProps) {
  const base: React.CSSProperties = {
    border: "none",
    borderRadius: 999,
    padding: "6px 14px",
    fontSize: 14,
    cursor: "pointer",
    display: "inline-flex",
    alignItems: "center",
    gap: 6,
  };

  const colors: Record<Variant, React.CSSProperties> = {
    primary: {
      background: "#2563eb",
      color: "#fff",
    },
    secondary: {
      background: "#e5e7eb",
      color: "#111827",
    },
    danger: {
      background: "#ef4444",
      color: "#fff",
    },
    ghost: {
      background: "transparent",
      color: "#111827",
      border: "1px solid #e5e7eb",
    },
  };

  return <button style={{ ...base, ...colors[variant], ...style }} {...props} />;
}
