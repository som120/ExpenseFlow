"use client";

import { useRouter } from "next/navigation";
import type { ReactNode } from "react";
import { useEffect } from "react";

import { useAuthStore } from "@/store/auth-store";

export function AuthGuard({ children }: { children: ReactNode }) {
  const router = useRouter();
  const token = useAuthStore((state) => state.token);
  const hydrated = useAuthStore((state) => state.hydrated);

  useEffect(() => {
    if (hydrated && !token) {
      router.replace("/auth/login");
    }
  }, [hydrated, token, router]);

  if (!hydrated) {
    return <div className="p-6 text-sm text-muted-foreground">Loading your workspace...</div>;
  }

  if (!token) {
    return <div className="p-6 text-sm text-muted-foreground">Redirecting to login...</div>;
  }

  return <>{children}</>;
}
