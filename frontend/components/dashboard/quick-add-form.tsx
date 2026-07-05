"use client";

import { useState } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";

import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { api } from "@/lib/api";
import { useAuthStore } from "@/store/auth-store";

export function QuickAddForm() {
  const token = useAuthStore((state) => state.token);
  const hydrated = useAuthStore((state) => state.hydrated);
  const queryClient = useQueryClient();
  const [description, setDescription] = useState("");
  const [amount, setAmount] = useState("");
  const mutation = useMutation({
    mutationFn: () =>
      api.createTransaction(token!, {
        transaction_type: "personal",
        category_name: "Others",
        amount,
        my_share: amount,
        description,
        payment_owner: "self",
        transaction_date: new Date().toISOString().slice(0, 10),
        participants: [],
      }),
    onSuccess: () => {
      setDescription("");
      setAmount("");
      queryClient.invalidateQueries({ queryKey: ["transactions"] });
      queryClient.invalidateQueries({ queryKey: ["summary"] });
    },
  });

  return (
    <Card>
      <div className="mb-4">
        <h3 className="text-lg font-semibold">Quick Add</h3>
        <p className="text-sm text-muted-foreground">Capture a personal expense quickly from the dashboard.</p>
      </div>
      <div className="grid gap-4 md:grid-cols-2">
        <div>
          <Label>Description</Label>
          <Input value={description} onChange={(e) => setDescription(e.target.value)} placeholder="Coffee" />
        </div>
        <div>
          <Label>Amount</Label>
          <Input value={amount} onChange={(e) => setAmount(e.target.value)} placeholder="250" />
        </div>
      </div>
      <Button className="mt-4 w-full" onClick={() => mutation.mutate()} disabled={!hydrated || !token || !description || !amount || mutation.isPending}>
        {mutation.isPending ? "Saving..." : "Save Transaction"}
      </Button>
      {mutation.error ? <p className="mt-3 text-sm text-red-400">{mutation.error.message}</p> : null}
    </Card>
  );
}
