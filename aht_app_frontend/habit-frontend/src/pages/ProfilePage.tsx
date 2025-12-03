import { useEffect, useState } from "react";
import { authApi } from "../api/authApi";
import { Layout } from "../components/Layout";
import { Card } from "../components/Card";
import { Button } from "../components/Button";

export default function ProfilePage() {
  const [email, setEmail] = useState("");
  const [telegramLinked, setTelegramLinked] = useState(false);
  const [telegramUsername, setTelegramUsername] = useState<string | null>(null);
  const [bindingCode, setBindingCode] = useState<string | null>(null);

  // URL бота — вынести в env позже
  const TELEGRAM_BOT_URL = "https://t.me/AtomicHabitsTrackerBot";

  async function loadProfile() {
    try {
      const res = await authApi.me();
      setEmail(res.data.email);
      setTelegramLinked(res.data.telegram_linked);
      setTelegramUsername(res.data.telegram_username || null);
    } catch (err) {
      console.error(err);
    }
  }

  useEffect(() => {
    (async () => {
      await loadProfile();
    })();
  }, []);

  async function generateCode() {
    try {
      const res = await authApi.generateBindCode();
      setBindingCode(res.data.code);
    } catch (err) {
      console.error(err);
    }
  }

  return (
    <Layout>
      <Card>
        <div style={{ padding: 20 }}>
          <h2>Профиль</h2>

          <p>
            <b>Email:</b> {email}
          </p>

          <p>
            <b>Telegram:</b>{" "}
            {telegramLinked ? (
              <>
                привязан ✔️
                {telegramUsername && (
                  <>
                    <br />
                    <i>@{telegramUsername}</i>
                  </>
                )}
              </>
            ) : (
              "не привязан ❗"
            )}
          </p>

          {/* 🔽 Блок привязки Telegram */}
          {!telegramLinked && (
            <div style={{ marginTop: 20, padding: 10, border: "1px solid #ccc", borderRadius: 6 }}>
              <h3>Привязка Telegram</h3>

              <Button onClick={generateCode}>Сгенерировать код</Button>

              {bindingCode && (
                <div style={{ marginTop: 12 }}>
                  <p>Отправьте этот код в Telegram боту:</p>
                  <h2 style={{ margin: "10px 0" }}>{bindingCode}</h2>

                  <a href={TELEGRAM_BOT_URL} target="_blank" rel="noopener noreferrer">
                    <Button>Открыть бота в Telegram</Button>
                  </a>
                </div>
              )}
            </div>
          )}

          <br />

          <Button onClick={loadProfile}>🔄 Обновить статус</Button>
        </div>
      </Card>
    </Layout>
  );
}
