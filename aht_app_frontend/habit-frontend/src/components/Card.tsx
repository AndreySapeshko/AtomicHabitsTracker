import type { ReactNode, CSSProperties } from "react";

type CardProps = {
  children: ReactNode;
  style?: CSSProperties;
};

export function Card({ children, style }: CardProps) {
  return (
    <div
      style={{
        padding: 16,
        borderRadius: 12,
        border: "1px solid #e0e0e0",
        background: "#ffffff",
        boxShadow: "0 1px 3px rgba(0,0,0,0.04)",
        ...style,
      }}
    >
      {children}
    </div>
  );
}
