import { useAuthStore } from "../store/authStore";
import { Link } from "react-router-dom";
import { Layout } from "../components/Layout";
import { Card } from "../components/Card";
import { Button } from "../components/Button";

export default function HomePage() {
  const access = useAuthStore((s) => s.access);

  if (!access) {
    return (
      <Layout>
        <Card>
          <h2>Добро пожаловать в Atomic Habits Tracker 👋</h2>
          <p>
            Это приложение помогает выстраивать полезные и приятные привычки, отслеживать прогресс и
            получать напоминания в Telegram.
          </p>

          <div style={{ marginTop: 20, display: "flex", gap: 10 }}>
            <Button onClick={() => (window.location.href = "/login")}>Войти</Button>
            <Button variant="secondary" onClick={() => (window.location.href = "/register")}>
              Регистрация
            </Button>
          </div>

          <p style={{ marginTop: 16, fontSize: 13, color: "#6b7280" }}>
            После регистрации привяжите Telegram в профиле, чтобы получать напоминания.
          </p>
        </Card>
      </Layout>
    );
  }

  return (
    <Layout>
      <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
        <Card>
          <h2>С возвращением! ✨</h2>
          <p>Загляните в свои привычки, посмотрите статистику и не забудьте отметить выполнение.</p>

          <div style={{ marginTop: 16, display: "flex", gap: 10, flexWrap: "wrap" }}>
            <Link to="/habits">
              <Button>Мои привычки</Button>
            </Link>
            <Link to="/habits/public">
              <Button variant="secondary">Публичные привычки</Button>
            </Link>
            <Link to="/profile">
              <Button variant="ghost">Профиль</Button>
            </Link>
          </div>
        </Card>
      </div>
    </Layout>
  );
}
