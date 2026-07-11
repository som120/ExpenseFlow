"use client";

import { CategoryBreakdownChart } from "@/components/analytics/category-breakdown-chart";
import { MonthlyTrendChart } from "@/components/analytics/monthly-trend-chart";
import { MetricCard } from "@/components/dashboard/metric-card";
import { Card } from "@/components/ui/card";
import { useAnalyticsQuery } from "@/hooks/use-dashboard-data";

export default function AnalyticsPage() {
  const { data } = useAnalyticsQuery();

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-semibold">Analytics</h2>
        <p className="text-sm text-muted-foreground">Track trends, categories, and friend-wise balances.</p>
      </div>
      <div className="grid gap-4 md:grid-cols-3">
        <MetricCard label="Top Spending Category" value={data?.top_spending_category ?? "N/A"} />
        <MetricCard label="Average Monthly Spend" value={`₹${data?.average_monthly_spend ?? "0.00"}`} />
        <MetricCard label="Highest Expense" value={`₹${data?.highest_expense ?? "0.00"}`} />
      </div>
      <div className="grid gap-6 xl:grid-cols-2">
        <MonthlyTrendChart data={data?.monthly_trends ?? []} />
        <CategoryBreakdownChart data={data?.category_breakdown ?? []} />
      </div>
      <Card>
        <h3 className="mb-4 text-lg font-semibold">Friend Balances</h3>
        <div className="space-y-3">
          {data?.friend_balances.map((item) => (
            <div key={`${item.direction}-${item.friend}`} className="flex items-center justify-between rounded-xl border p-3 text-sm">
              <span>{item.friend}</span>
              <span>{item.direction} · ₹{item.amount}</span>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
}
