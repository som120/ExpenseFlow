"use client";

import { MetricCard } from "@/components/dashboard/metric-card";
import { QuickAddForm } from "@/components/dashboard/quick-add-form";
import { TelegramLinkCard } from "@/components/layout/telegram-link-card";
import { Card } from "@/components/ui/card";
import { useSummaryQuery, useTransactionsQuery } from "@/hooks/use-dashboard-data";

export default function DashboardPage() {
  const summaryQuery = useSummaryQuery();
  const transactionsQuery = useTransactionsQuery();
  const summary = summaryQuery.data;
  const transactions = transactionsQuery.data ?? [];

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-semibold">Home</h2>
        <p className="text-sm text-muted-foreground">Your finance snapshot in one place.</p>
      </div>
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        <MetricCard label="Current Balance" value={`₹${summary?.current_balance ?? "0.00"}`} />
        <MetricCard label="Total Income" value={`₹${summary?.total_income ?? "0.00"}`} />
        <MetricCard label="Total Expenses" value={`₹${summary?.total_expenses ?? "0.00"}`} />
        <MetricCard label="Net Savings" value={`₹${summary?.net_savings ?? "0.00"}`} />
        <MetricCard label="Money You Owe" value={`₹${summary?.money_you_owe ?? "0.00"}`} />
        <MetricCard label="Money Owed To You" value={`₹${summary?.money_owed_to_you ?? "0.00"}`} />
      </div>
      <div className="grid gap-6 xl:grid-cols-[1.2fr_0.8fr]">
        <Card>
          <h3 className="text-lg font-semibold">Recent Transactions</h3>
          <div className="mt-4 space-y-3 text-sm text-muted-foreground">
            {transactions.slice(0, 5).map((transaction) => (
              <div key={transaction.id} className="flex items-center justify-between rounded-xl border p-3">
                <span>{transaction.description}</span>
                <span>₹{transaction.amount}</span>
              </div>
            ))}
          </div>
        </Card>
        <div className="space-y-6">
          <QuickAddForm />
          <TelegramLinkCard />
        </div>
      </div>
    </div>
  );
}
