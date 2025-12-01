import { NavLink, useNavigate } from "react-router-dom";
import { useAuthStore } from "../store/authStore";

export function NavBar() {
  const access = useAuthStore((s) => s.access);
  const logout = useAuthStore((s) => s.logout);
  const navigate = useNavigate();

  if (!access) return null; // скрываем навбар для гостей

  return (
    <nav
      style={{
        display: "flex",
        alignItems: "center",
        gap: 20,
        padding: "10px 20px",
        background: "#f6f6f6",
        borderBottom: "1px solid #ddd",
      }}
    >
      <h3 style={{ margin: 0 }}>Habit Tracker</h3>

      <NavLink
        to="/"
        style={({ isActive }) => ({
          fontWeight: isActive ? "bold" : "normal",
          textDecoration: "none",
        })}
      >
        Главная
      </NavLink>

      <NavLink
        to="/habits"
        style={({ isActive }) => ({
          fontWeight: isActive ? "bold" : "normal",
          textDecoration: "none",
        })}
      >
        Привычки
      </NavLink>

      <NavLink
        to="/habits/public"
        style={({ isActive }) => ({
          fontWeight: isActive ? "bold" : "normal",
          textDecoration: "none",
        })}
      >
        Публичные
      </NavLink>

      <div style={{ flexGrow: 1 }} />

      <button
        onClick={() => {
          logout();
          navigate("/login");
        }}
        style={{
          background: "#ff4d4d",
          color: "white",
          border: "none",
          padding: "6px 12px",
          borderRadius: 6,
          cursor: "pointer",
        }}
      >
        Выйти
      </button>
    </nav>
  );
}
