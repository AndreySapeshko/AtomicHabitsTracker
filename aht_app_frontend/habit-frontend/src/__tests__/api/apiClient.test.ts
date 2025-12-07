import { describe, it, expect, vi } from "vitest";
import type { AuthState } from "../../store/authStore";

// 1. Мокаем store ДО импорта apiClient
vi.mock("../../store/authStore", () => ({
  useAuthStore: {
    getState: vi.fn<() => AuthState>(),
  },
}));

import { useAuthStore } from "../../store/authStore";
import { apiClient } from "../../api/apiClient";

// 2. Тип для конфигурации, с которой будет работать интерцептор
type TestConfig = {
  headers?: Record<string, string>;
};

// 3. Тип для доступа к внутренним handler'ам интерцептора
type RequestHandler = {
  fulfilled?: (config: TestConfig) => TestConfig;
};

type RequestInterceptorManager = {
  handlers: RequestHandler[];
};

// 4. Приводим useAuthStore к виду с мокнутым getState
type UseAuthStoreMock = {
  getState: ReturnType<typeof vi.fn<() => AuthState>>;
};

const mockedUseAuthStore = useAuthStore as unknown as UseAuthStoreMock;

// 5. Достаём первый request-интерцептор
function getRequestFulfilledHandler(): (config: TestConfig) => TestConfig {
  const manager = apiClient.interceptors.request as unknown as RequestInterceptorManager;

  const handler = manager.handlers.find((h) => h.fulfilled !== undefined);

  if (!handler || !handler.fulfilled) {
    throw new Error("Не найден request interceptor у apiClient");
  }

  return handler.fulfilled;
}

describe("apiClient Authorization interceptor", () => {
  it("adds Authorization header when token exists", () => {
    // Настраиваем store: токен есть
    mockedUseAuthStore.getState.mockReturnValue({
      access: "ABC123",
      refresh: null,
      setTokens: () => {},
      logout: () => {},
    });

    const fulfilled = getRequestFulfilledHandler();

    const config: TestConfig = {
      headers: {},
    };

    const result = fulfilled(config);

    expect(result.headers?.Authorization).toBe("Bearer ABC123");
  });

  it("does NOT add Authorization header when token is missing", () => {
    // Настраиваем store: токена нет
    mockedUseAuthStore.getState.mockReturnValue({
      access: null,
      refresh: null,
      setTokens: () => {},
      logout: () => {},
    });

    const fulfilled = getRequestFulfilledHandler();

    const config: TestConfig = {
      headers: {},
    };

    const result = fulfilled(config);

    expect(result.headers?.Authorization).toBeUndefined();
  });
});
