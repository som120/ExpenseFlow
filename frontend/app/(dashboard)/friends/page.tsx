"use client";

import { useState } from "react";

import { FriendForm } from "@/components/friends/friend-form";
import { FriendList } from "@/components/friends/friend-list";
import { useFriendsQuery } from "@/hooks/use-dashboard-data";

export default function FriendsPage() {
  const [fromDate, setFromDate] = useState("");
  const [toDate, setToDate] = useState("");
  const { data } = useFriendsQuery({ fromDate, toDate });

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-semibold">Friends</h2>
        <p className="text-sm text-muted-foreground">Track split balances and manage friend contacts.</p>
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
      <FriendForm />
      <FriendList friends={data ?? []} />
    </div>
  );
}
