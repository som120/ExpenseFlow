"use client";

import { useQuery } from "@tanstack/react-query";

import { api } from "@/lib/api";
import { useAuthStore } from "@/store/auth-store";

export function useSummaryQuery() {
  const token = useAuthStore((state) => state.token);
  const hydrated = useAuthStore((state) => state.hydrated);
  return useQuery({
    queryKey: ["summary", token],
    queryFn: () => api.summary(token!),
    enabled: hydrated && Boolean(token),
  });
}

export function useTransactionsQuery() {
  const token = useAuthStore((state) => state.token);
  const hydrated = useAuthStore((state) => state.hydrated);
  return useQuery({
    queryKey: ["transactions", token],
    queryFn: () => api.transactions(token!),
    enabled: hydrated && Boolean(token),
  });
}

export function useFriendsQuery() {
  const token = useAuthStore((state) => state.token);
  const hydrated = useAuthStore((state) => state.hydrated);
  return useQuery({
    queryKey: ["friends", token],
    queryFn: () => api.friends(token!),
    enabled: hydrated && Boolean(token),
  });
}

export function useBudgetsQuery() {
  const token = useAuthStore((state) => state.token);
  const hydrated = useAuthStore((state) => state.hydrated);
  return useQuery({
    queryKey: ["budgets", token],
    queryFn: () => api.budgets(token!),
    enabled: hydrated && Boolean(token),
  });
}

export function useAnalyticsQuery() {
  const token = useAuthStore((state) => state.token);
  const hydrated = useAuthStore((state) => state.hydrated);
  return useQuery({
    queryKey: ["analytics", token],
    queryFn: () => api.analytics(token!),
    enabled: hydrated && Boolean(token),
  });
}

export function useReportsQuery() {
  const token = useAuthStore((state) => state.token);
  const hydrated = useAuthStore((state) => state.hydrated);
  return useQuery({
    queryKey: ["reports", token],
    queryFn: () => api.reports(token!),
    enabled: hydrated && Boolean(token),
  });
}
