"use client";

import { TransactionTable } from "@/components/transactions/transaction-table";
import { useTransactionsQuery } from "@/hooks/use-dashboard-data";

export default function TransactionsPage() {
  const { data } = useTransactionsQuery();

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-semibold">Transactions</h2>
        <p className="text-sm text-muted-foreground">Search, filter, and manage all your entries.</p>
      </div>
      <TransactionTable transactions={data ?? []} />
    </div>
  );
}
