"use client";

import { useRouter } from "next/navigation";

import { useAuthStore } from "@/store/auth-store";
import { Button } from "@/components/ui/button";

export function Topbar() {
  const router = useRouter();
  const user = useAuthStore((state) => state.user);
  const clearAuth = useAuthStore((state) => state.clearAuth);

  const handleLogout = () => {
    clearAuth();
    router.replace("/auth/login");
  };

  return (
    <header className="flex items-center justify-between border-b bg-background/80 px-6 py-4 backdrop-blur">
      <div>
        <p className="text-sm text-muted-foreground">Welcome back</p>
        <h1 className="text-lg font-semibold">{user?.full_name ?? "Guest"}</h1>
      </div>
      <Button variant="secondary" onClick={handleLogout}>
        Logout
      </Button>
    </header>
  );
}
