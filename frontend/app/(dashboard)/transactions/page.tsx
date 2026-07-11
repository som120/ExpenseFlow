"use client";

import { useState } from "react";

import { TransactionForm } from "@/components/transactions/transaction-form";
import { TransactionTable } from "@/components/transactions/transaction-table";
import { useTransactionsQuery } from "@/hooks/use-dashboard-data";
import type { Transaction } from "@/types";

export default function TransactionsPage() {
  const { data } = useTransactionsQuery();
  const [selectedTransaction, setSelectedTransaction] = useState<Transaction | null>(null);

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-semibold">Transactions</h2>
        <p className="text-sm text-muted-foreground">Search, filter, and manage all your entries.</p>
      </div>
      <TransactionForm selected={selectedTransaction} onDone={() => setSelectedTransaction(null)} />
      <TransactionTable transactions={data ?? []} onEdit={(transaction) => setSelectedTransaction(transaction)} />
    </div>
  );
}
