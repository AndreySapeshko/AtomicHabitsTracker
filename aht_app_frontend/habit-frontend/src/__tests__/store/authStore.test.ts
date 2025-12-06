import { useAuthStore } from "../../store/authStore";

const ACCESS_KEY = "access_token";
const REFRESH_KEY = "refresh_token";

beforeEach(() => {
  localStorage.clear();
  useAuthStore.setState({ access: null, refresh: null });
});

test("setTokens stores tokens in localStorage and state", () => {
  const store = useAuthStore.getState();

  store.setTokens("ACCESS123", "REFRESH456");

  // Проверяем state
  expect(useAuthStore.getState().access).toBe("ACCESS123");
  expect(useAuthStore.getState().refresh).toBe("REFRESH456");

  // Проверяем localStorage
  expect(localStorage.getItem(ACCESS_KEY)).toBe("ACCESS123");
  expect(localStorage.getItem(REFRESH_KEY)).toBe("REFRESH456");
});

test("logout clears tokens", () => {
  const store = useAuthStore.getState();

  // подготовка
  store.setTokens("AAA", "BBB");

  // действие
  store.logout();

  // state
  expect(useAuthStore.getState().access).toBeNull();
  expect(useAuthStore.getState().refresh).toBeNull();

  // localStorage
  expect(localStorage.getItem(ACCESS_KEY)).toBeNull();
  expect(localStorage.getItem(REFRESH_KEY)).toBeNull();
});
