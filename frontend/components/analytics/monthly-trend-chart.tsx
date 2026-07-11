"use client";

import { Area, AreaChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

import { Card } from "@/components/ui/card";
import type { TrendPoint } from "@/types";

export function MonthlyTrendChart({ data }: { data: TrendPoint[] }) {
  return (
    <Card>
      <h3 className="mb-4 text-lg font-semibold">Monthly Trends</h3>
      <div className="h-80">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={data}>
            <CartesianGrid strokeDasharray="3 3" strokeOpacity={0.2} />
            <XAxis dataKey="label" />
            <YAxis />
            <Tooltip />
            <Area type="monotone" dataKey="income" stroke="#10b981" fill="#10b98133" />
            <Area type="monotone" dataKey="expenses" stroke="#f97316" fill="#f9731633" />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </Card>
  );
}
