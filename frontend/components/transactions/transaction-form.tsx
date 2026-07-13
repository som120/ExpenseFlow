"use client";

import { useEffect, useMemo, useState } from "react";

import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useCategoriesQuery } from "@/hooks/use-dashboard-data";
import { useFriendsQuery } from "@/hooks/use-dashboard-data";
import { useCreateTransaction, useUpdateTransaction } from "@/hooks/use-management";
import type { Transaction } from "@/types";

const today = new Date().toISOString().slice(0, 10);

export function TransactionForm({ selected, onDone }: { selected?: Transaction | null; onDone?: () => void }) {
  const createTransaction = useCreateTransaction();
  const updateTransaction = useUpdateTransaction();
  const { data: friends } = useFriendsQuery();
  const { data: categories } = useCategoriesQuery();
  const [transactionType, setTransactionType] = useState("personal");
  const [description, setDescription] = useState("");
  const [amount, setAmount] = useState("");
  const [myShare, setMyShare] = useState("");
  const [categoryName, setCategoryName] = useState("Others");
  const [paymentOwner, setPaymentOwner] = useState("self");
  const [transactionDate, setTransactionDate] = useState(today);
  const [participantNames, setParticipantNames] = useState("");
  const [participantShareMap, setParticipantShareMap] = useState<Record<string, string>>({});
  const friendOptions = useMemo(() => friends ?? [], [friends]);

  const resetForm = () => {
    setTransactionType("personal");
    setDescription("");
    setAmount("");
    setMyShare("");
    setCategoryName("Others");
    setPaymentOwner("self");
    setTransactionDate(today);
    setParticipantNames("");
  };

  useEffect(() => {
    if (!selected) {
      resetForm();
      return;
    }

    setTransactionType(selected.transaction_type);
    setDescription(selected.description);
    setAmount(selected.amount);
    setMyShare(selected.my_share);
    setCategoryName(selected.category_name ?? "Others");
    setPaymentOwner(selected.payment_owner);
    setTransactionDate(selected.transaction_date);
    setParticipantNames(selected.participants.map((participant) => participant.participant_name).join(", "));
    setParticipantShareMap(
      Object.fromEntries(selected.participants.map((participant) => [participant.participant_name, participant.share_amount]))
    );
  }, [selected]);

  useEffect(() => {
    if (transactionType === "personal") {
      setMyShare(amount);
      setPaymentOwner("self");
    }

    if (transactionType === "income") {
      setMyShare(amount);
    }
  }, [transactionType, amount]);

  const mutation = selected ? updateTransaction : createTransaction;

  const handleSubmit = () => {
    const participantList = participantNames
      .split(",")
      .map((item) => item.trim())
      .filter(Boolean);
    const equalShareAmount = participantList.length > 0 ? (Number(amount) / (participantList.length + 1)).toFixed(2) : "0.00";

    const payload = {
      transaction_type: transactionType,
      category_name: categoryName,
      amount,
      my_share: transactionType === "personal" || transactionType === "income" ? amount : (myShare || amount),
      description,
      payment_owner: paymentOwner,
      transaction_date: transactionDate,
      participants:
        transactionType === "shared" || transactionType === "borrowed"
          ? participantList.map((name) => ({
              friend_id: friendOptions.find((friend) => friend.name === name)?.id,
              participant_name: name,
              share_amount: participantShareMap[name] || equalShareAmount,
              pending_amount: participantShareMap[name] || equalShareAmount,
              status: "pending",
            }))
          : [],
    };

    if (selected) {
      updateTransaction.mutate(
        { transactionId: selected.id, payload },
        { onSuccess: () => onDone?.() },
      );
      return;
    }

    createTransaction.mutate(payload, { onSuccess: () => { resetForm(); onDone?.(); } });
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
          <Label>Description</Label>
          <Input value={description} onChange={(e) => setDescription(e.target.value)} placeholder="Coffee" />
        </div>
        <div>
          <Label>Amount</Label>
          <Input value={amount} onChange={(e) => setAmount(e.target.value)} placeholder="250" />
        </div>
        <div>
          <Label>My Share</Label>
          <Input
            value={myShare}
            onChange={(e) => setMyShare(e.target.value)}
            placeholder="250"
            disabled={transactionType === "personal" || transactionType === "income"}
          />
        </div>
        <div>
          <Label>Payment Owner</Label>
          <Input value={paymentOwner} onChange={(e) => setPaymentOwner(e.target.value)} placeholder="self" />
        </div>
        <div>
          <Label>Date</Label>
          <Input type="date" value={transactionDate} onChange={(e) => setTransactionDate(e.target.value)} />
        </div>
        {(transactionType === "shared" || transactionType === "borrowed") && (
          <div className="md:col-span-2">
            <Label>Participants</Label>
            <div className="mb-2 flex flex-wrap gap-2 text-xs text-muted-foreground">
              {friendOptions.map((friend) => (
                <button
                  key={friend.id}
                  type="button"
                  className="rounded-full border px-2 py-1"
                  onClick={() => {
                    const current = participantNames.split(",").map((item) => item.trim()).filter(Boolean);
                    if (!current.includes(friend.name)) {
                      setParticipantNames([...current, friend.name].join(", "));
                    }
                  }}
                >
                  {friend.name}
                </button>
              ))}
            </div>
            <Input
              value={participantNames}
              onChange={(e) => {
                setParticipantNames(e.target.value);
                const names = e.target.value.split(",").map((item) => item.trim()).filter(Boolean);
                setParticipantShareMap((current) => {
                  const next: Record<string, string> = {};
                  for (const name of names) {
                    next[name] = current[name] ?? "";
                  }
                  return next;
                });
              }}
              placeholder={friends?.length ? friends.map((friend) => friend.name).join(", ") : "Om, Rahul"}
            />
            <p className="mt-1 text-xs text-muted-foreground">Comma-separated names for equal split.</p>
            <div className="mt-3 grid gap-3 md:grid-cols-2">
              {participantNames.split(",").map((item) => item.trim()).filter(Boolean).map((name) => (
                <div key={name}>
                  <Label>{name} share</Label>
                  <Input
                    value={participantShareMap[name] ?? ""}
                    onChange={(e) => setParticipantShareMap((current) => ({ ...current, [name]: e.target.value }))}
                    placeholder="20"
                  />
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
      <Button className="mt-4" onClick={handleSubmit} disabled={mutation.isPending || !description || !amount}>
        {mutation.isPending ? "Saving..." : selected ? "Update Transaction" : "Create Transaction"}
      </Button>
      {mutation.error ? <p className="mt-3 text-sm text-red-400">{mutation.error.message}</p> : null}
    </Card>
  );
}
