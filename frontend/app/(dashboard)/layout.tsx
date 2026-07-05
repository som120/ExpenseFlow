import { AuthGuard } from "@/components/layout/auth-guard";
import { Sidebar } from "@/components/layout/sidebar";
import { Topbar } from "@/components/layout/topbar";
import type { ReactNode } from "react";

export default function DashboardLayout({ children }: { children: ReactNode }) {
  return (
    <AuthGuard>
      <div className="min-h-screen bg-background text-foreground lg:grid lg:grid-cols-[16rem_1fr]">
        <Sidebar />
        <div>
          <Topbar />
          <main className="p-6">{children}</main>
        </div>
      </div>
    </AuthGuard>
  );
}
