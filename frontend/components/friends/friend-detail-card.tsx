"use client";

import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { useFriendHistoryQuery } from "@/hooks/use-dashboard-data";
import { useSettleFriend } from "@/hooks/use-management";

export function FriendDetailCard({ friendId, fromDate, toDate }: { friendId: string; fromDate?: string; toDate?: string }) {
  const { data } = useFriendHistoryQuery(friendId, { fromDate, toDate });
  const settleFriend = useSettleFriend();

  if (!data) {
    return null;
  }

  return (
    <Card>
      <div className="mb-4 flex items-center justify-between">
        <div>
          <h3 className="text-lg font-semibold">{data.name}</h3>
          <p className="text-sm text-muted-foreground">Owes you ₹{data.total_owed_to_you ?? "0.00"} · You owe ₹{data.total_you_owe ?? "0.00"}</p>
        </div>
        <Button variant="secondary" onClick={() => settleFriend.mutate({ friendId })}>Settle All</Button>
      </div>
      <div className="space-y-3">
        {data.history.map((item) => (
          <div key={`${item.transaction_id}-${item.transaction_date}`} className="rounded-xl border p-3 text-sm">
            <div className="flex items-center justify-between">
              <div>
                <p className="font-medium">{item.description}</p>
                <p className="text-muted-foreground">{item.transaction_date} · {item.transaction_type}</p>
              </div>
              <div className="text-right">
                <p>Share ₹{item.share_amount}</p>
                <p>Pending ₹{item.pending_amount}</p>
              </div>
            </div>
            {item.pending_amount !== "0.00" ? (
              <Button className="mt-3" variant="ghost" onClick={() => settleFriend.mutate({ friendId, transactionId: item.transaction_id })}>
                Mark Settled
              </Button>
            ) : (
              <p className="mt-3 text-xs text-green-400">Settled</p>
            )}
          </div>
        ))}
      </div>
    </Card>
  );
}
