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
        </Card>
      ))}
    </div>
  );
}
