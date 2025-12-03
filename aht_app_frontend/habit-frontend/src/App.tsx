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
import HabitAnalyticsPage from "./pages/HabitAnalyticsPage";
import PublicHabitsPage from "./pages/PublicHabitsPage";
import HomePage from "./pages/HomePage";
import ProfilePage from "./pages/ProfilePage";

function App() {
  return (
    <BrowserRouter>
      <NavBar />

      <Routes>
        <Route path="/" element={<HomePage />} />

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

        <Route
          path="/habits/:id/analytics"
          element={
            <ProtectedRoute>
              <HabitAnalyticsPage />
            </ProtectedRoute>
          }
        />

        <Route
          path="/profile"
          element={
            <ProtectedRoute>
              <ProfilePage />
            </ProtectedRoute>
          }
        />

        <Route path="/habits/public" element={<PublicHabitsPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
