"use client";

import Link from "next/link";
import type { Route } from "next";
import { BarChart3, FileText, LayoutDashboard, Receipt, Users, Wallet } from "lucide-react";

const items: Array<{ href: Route; label: string; icon: typeof LayoutDashboard }> = [
  { href: "/", label: "Dashboard", icon: LayoutDashboard },
  { href: "/transactions", label: "Transactions", icon: Receipt },
  { href: "/friends", label: "Friends", icon: Users },
  { href: "/budgets", label: "Budgets", icon: Wallet },
  { href: "/analytics", label: "Analytics", icon: BarChart3 },
  { href: "/reports", label: "Reports", icon: FileText },
];

export function Sidebar() {
  return (
    <aside className="hidden w-64 flex-col border-r bg-card/30 p-4 lg:flex">
      <div className="mb-8 text-xl font-semibold">ExpenseFlow</div>
      <nav className="space-y-2">
        {items.map(({ href, label, icon: Icon }) => (
          <Link
            key={href}
            href={href}
            className="flex items-center gap-3 rounded-xl px-3 py-2 text-sm text-muted-foreground hover:bg-accent hover:text-accent-foreground"
          >
            <Icon className="h-4 w-4" />
            {label}
          </Link>
        ))}
      </nav>
    </aside>
  );
}
