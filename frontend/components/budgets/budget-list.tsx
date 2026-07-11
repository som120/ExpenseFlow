"use client";

import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { useDeleteBudget } from "@/hooks/use-management";
import type { Budget } from "@/types";

export function BudgetList({ budgets }: { budgets: Budget[] }) {
  const deleteBudget = useDeleteBudget();

  return (
    <div className="grid gap-4 md:grid-cols-2">
      {budgets.map((budget) => {
        const spent = Number(budget.spent_amount);
        const amount = Number(budget.amount);
        const progress = amount > 0 ? Math.min((spent / amount) * 100, 100) : 0;

        return (
          <Card key={budget.id}>
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-lg font-semibold">{budget.name}</h3>
                <p className="text-sm text-muted-foreground">{budget.category_name ?? "Overall"} · {budget.period}</p>
              </div>
              <p className="text-sm font-medium">₹{budget.remaining_amount} left</p>
            </div>
            <div className="mt-4 h-3 rounded-full bg-accent">
              <div className="h-3 rounded-full bg-primary" style={{ width: `${progress}%` }} />
            </div>
            <p className="mt-3 text-sm text-muted-foreground">Spent ₹{budget.spent_amount} of ₹{budget.amount}</p>
            <Button className="mt-4" variant="ghost" onClick={() => deleteBudget.mutate(budget.id)}>
              Delete Budget
            </Button>
          </Card>
        );
      })}
    </div>
  );
}
