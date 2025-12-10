import { useState } from "react";
import { authApi } from "../api/authApi";
import { useAuthStore } from "../store/authStore";
import { useNavigate } from "react-router-dom";
import { AxiosError } from "axios";
import { Layout } from "../components/Layout";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);

  const setTokens = useAuthStore((s) => s.setTokens);
  const navigate = useNavigate();

  const login = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    try {
      const response = await authApi.login({ email, password });

      const { access, refresh } = response.data;
      setTokens(access, refresh);

      navigate("/");
    } catch (err: unknown) {
      if (err instanceof AxiosError) {
        setError(err.response?.data?.detail || "Ошибка входа");
      } else {
        setError("Неизвестная ошибка");
      }
    }
  };

  return (
    <Layout>
      <div style={{ padding: 20 }}>
        <h2>Вход</h2>

        <form onSubmit={login}>
          <div>
            <label htmlFor="email">Email</label>
            <br />
            <input
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              type="email"
            />
          </div>

          <div style={{ marginTop: 10 }}>
            <label htmlFor="password">Пароль</label>
            <br />
            <input
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              type="password"
            />
          </div>

          {error && <div style={{ marginTop: 10, color: "red" }}>{error}</div>}

          <button style={{ marginTop: 15 }} type="submit">
            Войти
          </button>
        </form>
      </div>
    </Layout>
  );
}
