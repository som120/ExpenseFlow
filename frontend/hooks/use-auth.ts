"use client";

import { useMutation } from "@tanstack/react-query";
import { useRouter } from "next/navigation";

import { api } from "@/lib/api";
import { useAuthStore } from "@/store/auth-store";

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
