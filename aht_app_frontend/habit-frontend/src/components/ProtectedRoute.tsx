import type { ReactNode } from "react";
import { Navigate } from "react-router-dom";
import { useAuthStore } from "../store/authStore";

type Props = {
  children: ReactNode;
};

export function ProtectedRoute({ children }: Props) {
  const access = useAuthStore((s) => s.access);

  if (!access) {
    return <Navigate to="/login" replace />;
  }

  return <>{children}</>;
}
