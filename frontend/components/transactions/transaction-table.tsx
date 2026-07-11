"use client";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { useDeleteTransaction } from "@/hooks/use-management";
import type { Transaction } from "@/types";

export function TransactionTable({ transactions, onEdit }: { transactions: Transaction[]; onEdit?: (transaction: Transaction) => void }) {
  const deleteTransaction = useDeleteTransaction();

  return (
    <Card className="overflow-hidden p-0">
      <table className="w-full text-left text-sm">
        <thead className="bg-accent/40 text-muted-foreground">
          <tr>
            <th className="px-4 py-3">Description</th>
            <th className="px-4 py-3">Type</th>
            <th className="px-4 py-3">Category</th>
            <th className="px-4 py-3">Amount</th>
            <th className="px-4 py-3">My Share</th>
            <th className="px-4 py-3">Actions</th>
          </tr>
        </thead>
        <tbody>
          {transactions.map((transaction) => (
            <tr key={transaction.id} className="border-t">
              <td className="px-4 py-3">{transaction.description}</td>
              <td className="px-4 py-3"><Badge>{transaction.transaction_type}</Badge></td>
              <td className="px-4 py-3">{transaction.category_name ?? "Others"}</td>
              <td className="px-4 py-3">₹{transaction.amount}</td>
              <td className="px-4 py-3">₹{transaction.my_share}</td>
              <td className="px-4 py-3">
                <div className="flex gap-2">
                  <Button variant="secondary" onClick={() => onEdit?.(transaction)}>Edit</Button>
                  <Button variant="ghost" onClick={() => deleteTransaction.mutate(transaction.id)}>Delete</Button>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </Card>
  );
}
