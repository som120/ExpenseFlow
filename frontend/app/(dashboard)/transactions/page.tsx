"use client";

import { useState } from "react";

import { TransactionForm } from "@/components/transactions/transaction-form";
import { TransactionTable } from "@/components/transactions/transaction-table";
import { useTransactionsQuery } from "@/hooks/use-dashboard-data";
import type { Transaction } from "@/types";

export default function TransactionsPage() {
  const { data } = useTransactionsQuery();
  const [selectedTransaction, setSelectedTransaction] = useState<Transaction | null>(null);
  const [search, setSearch] = useState("");
  const [typeFilter, setTypeFilter] = useState("all");
  const [limit, setLimit] = useState("20");

  const filteredTransactions = (data ?? []).filter((transaction) => {
    const matchesSearch = transaction.description.toLowerCase().includes(search.toLowerCase())
      || (transaction.category_name ?? "").toLowerCase().includes(search.toLowerCase());
    const matchesType = typeFilter === "all" || transaction.transaction_type === typeFilter;
    return matchesSearch && matchesType;
  }).slice(0, Number(limit));

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-semibold">Transactions</h2>
        <p className="text-sm text-muted-foreground">Search, filter, and manage all your entries.</p>
      </div>
      <div className="grid gap-4 md:grid-cols-2">
        <input
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Search by description or category"
          className="flex h-11 w-full rounded-xl border bg-card px-3 py-2 text-sm"
        />
        <select
          value={typeFilter}
          onChange={(e) => setTypeFilter(e.target.value)}
          className="flex h-11 w-full rounded-xl border bg-card px-3 py-2 text-sm"
        >
          <option value="all">All types</option>
          <option value="personal">Personal</option>
          <option value="income">Income</option>
          <option value="shared">Shared</option>
          <option value="borrowed">Borrowed</option>
        </select>
      </div>
      <div className="max-w-xs">
        <label className="mb-2 block text-sm font-medium text-foreground">View transactions</label>
        <select
          value={limit}
          onChange={(e) => setLimit(e.target.value)}
          className="flex h-11 w-full rounded-xl border bg-card px-3 py-2 text-sm"
        >
          <option value="20">0-20</option>
          <option value="50">0-50</option>
          <option value="100">0-100</option>
        </select>
      </div>
      <TransactionForm selected={selectedTransaction} onDone={() => setSelectedTransaction(null)} />
      <TransactionTable transactions={filteredTransactions} onEdit={(transaction) => setSelectedTransaction(transaction)} />
    </div>
  );
}
