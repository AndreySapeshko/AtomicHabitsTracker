import { BrowserRouter, Routes, Route } from "react-router-dom";
import { NavBar } from "./components/NavBar";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import { ProtectedRoute } from "./components/ProtectedRoute";
import HabitsPage from "./pages/HabitsPage";
import HabitCreatePage from "./pages/HabitCreatePage";
import HabitEditPage from "./pages/HabitEditPage";
import HabitDetailsPage from "./pages/HabitDetailsPage";
import HabitInstancesPage from "./pages/HabitInstancesPage";

function App() {
  return (
    <BrowserRouter>
      <NavBar />

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

          <Route
            path="/habits/:id"
            element={
              <ProtectedRoute>
                <HabitDetailsPage />
              </ProtectedRoute>
            }
          />

          <Route
            path="/habits/:id/edit"
            element={
              <ProtectedRoute>
                <HabitEditPage />
              </ProtectedRoute>
            }
          />

          <Route
            path="/habits/:id"
            element={
              <ProtectedRoute>
                <HabitDetailsPage />
              </ProtectedRoute>
            }
          />

          <Route
            path="/habits/:id/instances"
            element={
              <ProtectedRoute>
                <HabitInstancesPage />
              </ProtectedRoute>
            }
          />

          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
        </Routes>
    </BrowserRouter>
  );
}

export default App;
