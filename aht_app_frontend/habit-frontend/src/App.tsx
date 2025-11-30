import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import { ProtectedRoute } from "./components/ProtectedRoute";
import HabitsPage from "./pages/HabitsPage";
import HabitCreatePage from "./pages/HabitCreatePage";

function App() {
  return (
    <BrowserRouter>
      <div style={{ padding: 20 }}>
        {/* НАВИГАЦИЯ */}
        <nav style={{ marginBottom: 20 }}>
          <Link to="/" style={{ marginRight: 10 }}>
            Главная
          </Link>
          <Link to="/habits" style={{ marginRight: 10 }}>
            Мои привычки
          </Link>
          <Link to="/login" style={{ marginRight: 10 }}>
            Логин
          </Link>
          <Link to="/register">Регистрация</Link>
        </nav>

        <Routes>
          <Route
            path="/"
            element={
              <ProtectedRoute>
                <div>Главная страница (личный кабинет будет здесь)</div>
              </ProtectedRoute>
            }
          />

          <Route
            path="/habits"
            element={
              <ProtectedRoute>
                <HabitsPage />
              </ProtectedRoute>
            }
          />

          <Route
            path="/habits/create"
            element={
              <ProtectedRoute>
                <HabitCreatePage />
              </ProtectedRoute>
            }
          />

          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;
