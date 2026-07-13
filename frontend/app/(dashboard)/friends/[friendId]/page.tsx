"use client";

import { use } from "react";
import { useState } from "react";

import { FriendDetailCard } from "@/components/friends/friend-detail-card";

export default function FriendDetailPage({ params }: { params: Promise<{ friendId: string }> }) {
  const resolvedParams = use(params);
  const [fromDate, setFromDate] = useState("");
  const [toDate, setToDate] = useState("");

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-semibold">Friend Detail</h2>
        <p className="text-sm text-muted-foreground">Review history and settle pending balances.</p>
      </div>
      <div className="grid gap-4 md:grid-cols-2">
        <input
          type="date"
          value={fromDate}
          onChange={(e) => setFromDate(e.target.value)}
          className="flex h-11 w-full rounded-xl border bg-card px-3 py-2 text-sm"
        />
        <input
          type="date"
          value={toDate}
          onChange={(e) => setToDate(e.target.value)}
          className="flex h-11 w-full rounded-xl border bg-card px-3 py-2 text-sm"
        />
      </div>
      <FriendDetailCard friendId={resolvedParams.friendId} fromDate={fromDate} toDate={toDate} />
    </div>
  );
}
