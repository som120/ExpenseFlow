"use client";

import Link from "next/link";

import { Card } from "@/components/ui/card";
import type { Friend } from "@/types";

export function FriendList({ friends }: { friends: Friend[] }) {
  return (
    <div className="grid gap-4 md:grid-cols-2">
      {friends.map((friend) => (
        <Card key={friend.id}>
          <h3 className="text-lg font-semibold">{friend.name}</h3>
          <p className="text-sm text-muted-foreground">@{friend.telegram_username ?? "not-set"}</p>
          <p className="mt-2 text-sm text-muted-foreground">{friend.notes ?? "No notes yet."}</p>
          <div className="mt-4 grid gap-2 text-sm">
            <p>Owes you: ₹{friend.total_owed_to_you ?? "0.00"}</p>
            <p>You owe: ₹{friend.total_you_owe ?? "0.00"}</p>
          </div>
          <Link href={`/friends/${friend.id}`} className="mt-4 inline-block text-sm text-primary">
            View history →
          </Link>
        </Card>
      ))}
    </div>
  );
}
