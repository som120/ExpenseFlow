"use client";

import { BudgetList } from "@/components/budgets/budget-list";
import { useBudgetsQuery } from "@/hooks/use-dashboard-data";

export default function BudgetsPage() {
  const { data } = useBudgetsQuery();

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-semibold">Budgets</h2>
        <p className="text-sm text-muted-foreground">Monitor your monthly and category spending limits.</p>
      </div>
      <BudgetList budgets={data ?? []} />
    </div>
  );
}
