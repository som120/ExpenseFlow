"use client";

import { useMutation, useQueryClient } from "@tanstack/react-query";

import { api } from "@/lib/api";
import { useAuthStore } from "@/store/auth-store";

function invalidateAll(queryClient: ReturnType<typeof useQueryClient>) {
  queryClient.invalidateQueries({ queryKey: ["transactions"] });
  queryClient.invalidateQueries({ queryKey: ["summary"] });
  queryClient.invalidateQueries({ queryKey: ["budgets"] });
  queryClient.invalidateQueries({ queryKey: ["analytics"] });
  queryClient.invalidateQueries({ queryKey: ["reports"] });
}

export function useCreateTransaction() {
  const token = useAuthStore((state) => state.token);
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (payload: unknown) => api.createTransaction(token!, payload),
    onSuccess: () => invalidateAll(queryClient),
  });
}

export function useUpdateTransaction() {
  const token = useAuthStore((state) => state.token);
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ transactionId, payload }: { transactionId: string; payload: unknown }) =>
      api.updateTransaction(token!, transactionId, payload),
    onSuccess: () => invalidateAll(queryClient),
  });
}

export function useDeleteTransaction() {
  const token = useAuthStore((state) => state.token);
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (transactionId: string) => api.deleteTransaction(token!, transactionId),
    onSuccess: () => invalidateAll(queryClient),
  });
}

export function useCreateBudget() {
  const token = useAuthStore((state) => state.token);
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (payload: unknown) => api.createBudget(token!, payload),
    onSuccess: () => invalidateAll(queryClient),
  });
}

export function useCreateFriend() {
  const token = useAuthStore((state) => state.token);
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (payload: unknown) => api.createFriend(token!, payload),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["friends"] }),
  });
}

export function useDeleteBudget() {
  const token = useAuthStore((state) => state.token);
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (budgetId: string) => api.deleteBudget(token!, budgetId),
    onSuccess: () => invalidateAll(queryClient),
  });
}
