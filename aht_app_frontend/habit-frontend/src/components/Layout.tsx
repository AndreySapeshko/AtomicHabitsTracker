import type { ReactNode } from "react";

type LayoutProps = {
  children: ReactNode;
};

export function Layout({ children }: LayoutProps) {
  return (
    <div
      style={{
        minHeight: "100vh",
        background: "#f5f5f7",
      }}
    >
      <div
        style={{
          maxWidth: 960,
          margin: "0 auto",
          padding: "20px 16px 40px",
        }}
      >
        {children}
      </div>
    </div>
  );
}
