"use client";

import { useMutation } from "@tanstack/react-query";
import { useRouter } from "next/navigation";

import { api } from "@/lib/api";
import { useAuthStore } from "@/store/auth-store";
import type { TelegramAuthPayload } from "@/types";

export function useLogin() {
  const router = useRouter();
  const setAuth = useAuthStore((state) => state.setAuth);

  return useMutation({
    mutationFn: async (payload: { email: string; password: string }) => {
      const tokenResponse = await api.login(payload);
      const user = await api.me(tokenResponse.access_token);
      return { token: tokenResponse.access_token, user };
    },
    onSuccess: ({ token, user }) => {
      setAuth(token, user);
      router.push("/");
    },
  });
}

export function useRegister() {
  const router = useRouter();

  return useMutation({
    mutationFn: (payload: { email: string; full_name: string; password: string }) => api.register(payload),
    onSuccess: () => {
      router.push("/auth/login");
    },
  });
}

export function useTelegramLogin() {
  const router = useRouter();
  const setAuth = useAuthStore((state) => state.setAuth);

  return useMutation({
    mutationFn: (payload: TelegramAuthPayload) => api.telegramLogin(payload),
    onSuccess: ({ access_token, user }) => {
      setAuth(access_token, user);
      router.push("/");
    },
  });
}

export function useTelegramLink() {
  const token = useAuthStore((state) => state.token);
  const setAuth = useAuthStore((state) => state.setAuth);

  return useMutation({
    mutationFn: async (payload: TelegramAuthPayload) => {
      if (!token) {
        throw new Error("Login required to link Telegram");
      }
      const user = await api.telegramLink(token, payload);
      setAuth(token, user);
      return user;
    },
  });
}
