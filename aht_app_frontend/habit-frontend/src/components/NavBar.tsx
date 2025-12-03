import { NavLink, useNavigate, useLocation } from "react-router-dom";
import { useAuthStore } from "../store/authStore";
import { Button } from "./Button";

export function NavBar() {
  const access = useAuthStore((s) => s.access);
  const logout = useAuthStore((s) => s.logout);
  const navigate = useNavigate();
  const location = useLocation();

  const isAuthPage =
    location.pathname.startsWith("/login") ||
    location.pathname.startsWith("/register");

  const linkStyle = ({ isActive }: { isActive: boolean }) => ({
    textDecoration: "none",
    color: isActive ? "#111827" : "#4b5563",
    fontWeight: isActive ? 600 : 500,
    fontSize: 14,
  });

  return (
    <nav
      style={{
        background: "#ffffff",
        borderBottom: "1px solid #e5e7eb",
        padding: "8px 16px",
      }}
    >
      <div
        style={{
          maxWidth: 960,
          margin: "0 auto",
          display: "flex",
          alignItems: "center",
          gap: 16,
        }}
      >
        <div
          style={{ fontWeight: 700, fontSize: 16, cursor: "pointer" }}
          onClick={() => navigate("/")}
        >
          Atomic Habits Tracker
        </div>

        {/* Линки слева */}
        {access && (
          <>
            <NavLink to="/" style={linkStyle}>
              Главная
            </NavLink>
            <NavLink to="/habits" style={linkStyle}>
              Привычки
            </NavLink>
            <NavLink to="/habits/public" style={linkStyle}>
              Публичные
            </NavLink>
            <NavLink to="/profile" style={linkStyle}>
              Профиль
            </NavLink>
          </>
        )}

        <div style={{ flexGrow: 1 }} />

        {/* Справа — в зависимости от авторизации */}
        {!access && !isAuthPage && (
          <>
            <Button
              variant="ghost"
              onClick={() => navigate("/login")}
              style={{ fontSize: 13 }}
            >
              Войти
            </Button>
            <Button
              variant="primary"
              onClick={() => navigate("/register")}
              style={{ fontSize: 13 }}
            >
              Регистрация
            </Button>
          </>
        )}

        {access && (
          <Button
            variant="ghost"
            onClick={() => {
              logout();
              navigate("/");
            }}
            style={{ fontSize: 13 }}
          >
            Выйти
          </Button>
        )}
      </div>
    </nav>
  );
}
