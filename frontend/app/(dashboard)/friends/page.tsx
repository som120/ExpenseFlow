"use client";

import { FriendList } from "@/components/friends/friend-list";
import { useFriendsQuery } from "@/hooks/use-dashboard-data";

export default function FriendsPage() {
  const { data } = useFriendsQuery();

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-semibold">Friends</h2>
        <p className="text-sm text-muted-foreground">Track split balances and manage friend contacts.</p>
      </div>
      <FriendList friends={data ?? []} />
    </div>
  );
}
