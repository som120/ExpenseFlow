"use client";

import { useEffect, useState } from "react";

import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useCreateTransaction, useUpdateTransaction } from "@/hooks/use-management";
import type { Transaction } from "@/types";

const today = new Date().toISOString().slice(0, 10);

export function TransactionForm({ selected, onDone }: { selected?: Transaction | null; onDone?: () => void }) {
  const createTransaction = useCreateTransaction();
  const updateTransaction = useUpdateTransaction();
  const [transactionType, setTransactionType] = useState("personal");
  const [description, setDescription] = useState("");
  const [amount, setAmount] = useState("");
  const [myShare, setMyShare] = useState("");
  const [categoryName, setCategoryName] = useState("Others");
  const [paymentOwner, setPaymentOwner] = useState("self");
  const [transactionDate, setTransactionDate] = useState(today);

  useEffect(() => {
    if (!selected) {
      setTransactionType("personal");
      setDescription("");
      setAmount("");
      setMyShare("");
      setCategoryName("Others");
      setPaymentOwner("self");
      setTransactionDate(today);
      return;
    }

    setTransactionType(selected.transaction_type);
    setDescription(selected.description);
    setAmount(selected.amount);
    setMyShare(selected.my_share);
    setCategoryName(selected.category_name ?? "Others");
    setPaymentOwner(selected.payment_owner);
    setTransactionDate(selected.transaction_date);
  }, [selected]);

  const mutation = selected ? updateTransaction : createTransaction;

  const handleSubmit = () => {
    const payload = {
      transaction_type: transactionType,
      category_name: categoryName,
      amount,
      my_share: myShare || amount,
      description,
      payment_owner: paymentOwner,
      transaction_date: transactionDate,
      participants: [],
    };

    if (selected) {
      updateTransaction.mutate(
        { transactionId: selected.id, payload },
        { onSuccess: () => onDone?.() },
      );
      return;
    }

    createTransaction.mutate(payload, { onSuccess: () => onDone?.() });
  };

  return (
    <Card>
      <div className="mb-4">
        <h3 className="text-lg font-semibold">{selected ? "Edit Transaction" : "Add Transaction"}</h3>
        <p className="text-sm text-muted-foreground">Manage expenses, income, and categories from one form.</p>
      </div>
      <div className="grid gap-4 md:grid-cols-2">
        <div>
          <Label>Type</Label>
          <select
            value={transactionType}
            onChange={(e) => setTransactionType(e.target.value)}
            className="flex h-11 w-full rounded-xl border bg-card px-3 py-2 text-sm"
          >
            <option value="personal">Personal Expense</option>
            <option value="income">Income</option>
            <option value="shared">Shared Expense</option>
            <option value="borrowed">Borrowed Expense</option>
          </select>
        </div>
        <div>
          <Label>Category</Label>
          <Input value={categoryName} onChange={(e) => setCategoryName(e.target.value)} placeholder="Food" />
        </div>
        <div>
          <Label>Description</Label>
          <Input value={description} onChange={(e) => setDescription(e.target.value)} placeholder="Coffee" />
        </div>
        <div>
          <Label>Amount</Label>
          <Input value={amount} onChange={(e) => setAmount(e.target.value)} placeholder="250" />
        </div>
        <div>
          <Label>My Share</Label>
          <Input value={myShare} onChange={(e) => setMyShare(e.target.value)} placeholder="250" />
        </div>
        <div>
          <Label>Payment Owner</Label>
          <Input value={paymentOwner} onChange={(e) => setPaymentOwner(e.target.value)} placeholder="self" />
        </div>
        <div>
          <Label>Date</Label>
          <Input type="date" value={transactionDate} onChange={(e) => setTransactionDate(e.target.value)} />
        </div>
      </div>
      <Button className="mt-4" onClick={handleSubmit} disabled={mutation.isPending || !description || !amount}>
        {mutation.isPending ? "Saving..." : selected ? "Update Transaction" : "Create Transaction"}
      </Button>
      {mutation.error ? <p className="mt-3 text-sm text-red-400">{mutation.error.message}</p> : null}
    </Card>
  );
}
