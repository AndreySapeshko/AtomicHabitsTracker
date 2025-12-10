import { useState } from "react";
import { authApi } from "../api/authApi";
import { useNavigate } from "react-router-dom";
import { AxiosError } from "axios";
import { Layout } from "../components/Layout";

export default function RegisterPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);

  const navigate = useNavigate();

  const register = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    try {
      await authApi.register({ email, password });

      alert("Регистрация успешна! Теперь войдите.");
      navigate("/login");
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
        <h2>Регистрация</h2>

        <form onSubmit={register}>
          <div>
            <label>Email</label>
            <br />
            <input value={email} onChange={(e) => setEmail(e.target.value)} type="email" />
          </div>

          <div style={{ marginTop: 10 }}>
            <label>Пароль</label>
            <br />
            <input value={password} onChange={(e) => setPassword(e.target.value)} type="password" />
          </div>

          {error && <div style={{ marginTop: 10, color: "red" }}>{error}</div>}

          <button style={{ marginTop: 15 }} type="submit">
            Зарегистрироваться
          </button>
        </form>
      </div>
    </Layout>
  );
}
