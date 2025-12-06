import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import LoginPage from "../../pages/LoginPage";
import type * as ReactRouter from "react-router-dom";
import type { useAuthStore as useAuthStoreOriginal } from "../../store/authStore";
import type { Mock } from "vitest";
import { AxiosError, AxiosHeaders } from "axios";

// --- МОК useNavigate ---
const mockNavigate = vi.fn();
vi.mock("react-router-dom", async () => {
  const actual: typeof ReactRouter = await vi.importActual("react-router-dom");
  return {
    ...actual,
    useNavigate: () => mockNavigate,
  };
});

// --- МОК authApi ---
vi.mock("../../api/authApi", () => ({
  authApi: {
    login: vi.fn(),
  },
}));
import { authApi } from "../../api/authApi";

// --- МОК Zustand authStore ---
type AuthState = ReturnType<typeof useAuthStoreOriginal.getState>;

const mockSetTokens = vi.fn();
const mockLogout = vi.fn();

const mockAuthState: AuthState = {
  access: null,
  refresh: null,
  setTokens: mockSetTokens,
  logout: mockLogout,
};

vi.mock("../../store/authStore", () => ({
  useAuthStore: (selector: (s: AuthState) => unknown) => selector(mockAuthState),
}));

describe("LoginPage", () => {
  beforeEach(() => {
    mockNavigate.mockReset();
    mockSetTokens.mockReset();
    mockLogout.mockReset();
    (authApi.login as unknown as Mock).mockReset();
  });

  test("успешный вход выполняется правильно", async () => {
    (authApi.login as Mock).mockResolvedValue({
      data: {
        access: "ACCESS_TOKEN",
        refresh: "REFRESH_TOKEN",
      },
    });

    render(
      <MemoryRouter>
        <LoginPage />
      </MemoryRouter>,
    );

    fireEvent.change(screen.getByLabelText(/email/i), {
      target: { value: "test@mail.com" },
    });
    fireEvent.change(screen.getByLabelText(/пароль/i), {
      target: { value: "123456" },
    });

    fireEvent.click(screen.getByText("Войти"));

    await waitFor(() => {
      expect(mockSetTokens).toHaveBeenCalledWith("ACCESS_TOKEN", "REFRESH_TOKEN");
    });

    expect(mockNavigate).toHaveBeenCalledWith("/");
  });

  test("отображает ошибку от сервера", async () => {
    const dummyHeaders = new AxiosHeaders();

    const dummyConfig = {
      headers: dummyHeaders,
      url: "auth/login/",
      method: "post" as const,
    };

    const axiosErr = new AxiosError(
      "Request failed",
      "400",
      dummyConfig,
      {},
      {
        data: { detail: "Неверные данные" },
        status: 400,
        statusText: "Bad Request",
        headers: dummyHeaders,
        config: dummyConfig,
      },
    );

    (authApi.login as Mock).mockRejectedValue(axiosErr);

    render(
      <MemoryRouter>
        <LoginPage />
      </MemoryRouter>,
    );

    fireEvent.change(screen.getByLabelText(/email/i), {
      target: { value: "wrong@mail.com" },
    });

    fireEvent.change(screen.getByLabelText(/пароль/i), {
      target: { value: "badpass" },
    });

    fireEvent.click(screen.getByText("Войти"));

    expect(await screen.findByText("Неверные данные")).toBeInTheDocument();
  });
});
