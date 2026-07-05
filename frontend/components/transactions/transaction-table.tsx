import { Badge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";
import type { Transaction } from "@/types";

export function TransactionTable({ transactions }: { transactions: Transaction[] }) {
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
            </tr>
          ))}
        </tbody>
      </table>
    </Card>
  );
}
