"use client";

import { useState } from "react";

import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useCategoriesQuery } from "@/hooks/use-dashboard-data";
import { useCreateBudget } from "@/hooks/use-management";

export function BudgetForm() {
  const createBudget = useCreateBudget();
  const { data: categories } = useCategoriesQuery();
  const [name, setName] = useState("");
  const [amount, setAmount] = useState("");
  const [categoryName, setCategoryName] = useState("Others");
  const [period, setPeriod] = useState("monthly");

  return (
    <Card>
      <div className="mb-4">
        <h3 className="text-lg font-semibold">Create Budget</h3>
        <p className="text-sm text-muted-foreground">Set category or overall budgets from the web app.</p>
      </div>
      <div className="grid gap-4 md:grid-cols-2">
        <div>
          <Label>Name</Label>
          <Input value={name} onChange={(e) => setName(e.target.value)} placeholder="Food Budget" />
        </div>
        <div>
          <Label>Amount</Label>
          <Input value={amount} onChange={(e) => setAmount(e.target.value)} placeholder="10000" />
        </div>
        <div>
          <Label>Category</Label>
          <select
            value={categoryName}
            onChange={(e) => setCategoryName(e.target.value)}
            className="flex h-11 w-full rounded-xl border bg-card px-3 py-2 text-sm"
          >
            {(categories ?? []).map((category) => (
              <option key={category.id} value={category.name}>{category.name}</option>
            ))}
          </select>
        </div>
        <div>
          <Label>Period</Label>
          <select value={period} onChange={(e) => setPeriod(e.target.value)} className="flex h-11 w-full rounded-xl border bg-card px-3 py-2 text-sm">
            <option value="monthly">Monthly</option>
            <option value="weekly">Weekly</option>
            <option value="yearly">Yearly</option>
          </select>
        </div>
      </div>
      <Button
        className="mt-4"
        onClick={() =>
          createBudget.mutate(
            { name, amount, category_name: categoryName, period, is_active: true },
            {
              onSuccess: () => {
                setName("");
                setAmount("");
                setCategoryName("Others");
                setPeriod("monthly");
              },
            },
          )
        }
        disabled={!name || !amount || createBudget.isPending}
      >
        {createBudget.isPending ? "Saving..." : "Create Budget"}
      </Button>
      {createBudget.error ? <p className="mt-3 text-sm text-red-400">{createBudget.error.message}</p> : null}
    </Card>
  );
}
