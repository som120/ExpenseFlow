import type { AuthUser, Budget, Friend, Summary, Transaction } from "@/types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api/v1";

async function request<T>(path: string, options: RequestInit = {}, token?: string): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...(options.headers ?? {}),
    },
    cache: "no-store",
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: "Request failed" }));
    throw new Error(error.detail ?? "Request failed");
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return response.json() as Promise<T>;
}

export const api = {
  register: (payload: { email: string; full_name: string; password: string }) =>
    request<AuthUser>("/auth/register", { method: "POST", body: JSON.stringify(payload) }),
  login: (payload: { email: string; password: string }) =>
    request<{ access_token: string; token_type: string }>("/auth/login", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  me: (token: string) => request<AuthUser>("/auth/me", {}, token),
  summary: (token: string) => request<Summary>("/summary", {}, token),
  transactions: (token: string) => request<Transaction[]>("/transactions", {}, token),
  createTransaction: (token: string, payload: unknown) =>
    request<Transaction>("/transactions", { method: "POST", body: JSON.stringify(payload) }, token),
  friends: (token: string) => request<Friend[]>("/friends", {}, token),
  createFriend: (token: string, payload: unknown) =>
    request<Friend>("/friends", { method: "POST", body: JSON.stringify(payload) }, token),
  budgets: (token: string) => request<Budget[]>("/budgets", {}, token),
  createBudget: (token: string, payload: unknown) =>
    request<Budget>("/budgets", { method: "POST", body: JSON.stringify(payload) }, token),
};
