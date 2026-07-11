"use client";

import { Cell, Pie, PieChart, ResponsiveContainer, Tooltip } from "recharts";

import { Card } from "@/components/ui/card";
import type { CategoryBreakdownItem } from "@/types";

const COLORS = ["#10b981", "#3b82f6", "#f97316", "#8b5cf6", "#ef4444", "#14b8a6"];

export function CategoryBreakdownChart({ data }: { data: CategoryBreakdownItem[] }) {
  return (
    <Card>
      <h3 className="mb-4 text-lg font-semibold">Category Breakdown</h3>
      <div className="h-80">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie data={data} dataKey="amount" nameKey="category" outerRadius={110}>
              {data.map((entry, index) => (
                <Cell key={entry.category} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </Card>
  );
}
