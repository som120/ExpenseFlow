"use client";

import { useState } from "react";

import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useCreateFriend } from "@/hooks/use-management";

export function FriendForm() {
  const createFriend = useCreateFriend();
  const [name, setName] = useState("");
  const [telegramUsername, setTelegramUsername] = useState("");
  const [phone, setPhone] = useState("");
  const [notes, setNotes] = useState("");

  return (
    <Card>
      <div className="mb-4">
        <h3 className="text-lg font-semibold">Add Friend</h3>
        <p className="text-sm text-muted-foreground">Create friends to use in shared and borrowed expense flows.</p>
      </div>
      <div className="grid gap-4 md:grid-cols-2">
        <div>
          <Label>Name</Label>
          <Input value={name} onChange={(e) => setName(e.target.value)} placeholder="Om" />
        </div>
        <div>
          <Label>Telegram Username</Label>
          <Input value={telegramUsername} onChange={(e) => setTelegramUsername(e.target.value)} placeholder="om_friend" />
        </div>
        <div>
          <Label>Phone</Label>
          <Input value={phone} onChange={(e) => setPhone(e.target.value)} placeholder="9876543210" />
        </div>
        <div>
          <Label>Notes</Label>
          <Input value={notes} onChange={(e) => setNotes(e.target.value)} placeholder="College friend" />
        </div>
      </div>
      <Button
        className="mt-4"
        onClick={() =>
          createFriend.mutate(
            { name, telegram_username: telegramUsername || null, phone: phone || null, notes: notes || null },
            {
              onSuccess: () => {
                setName("");
                setTelegramUsername("");
                setPhone("");
                setNotes("");
              },
            },
          )
        }
        disabled={!name || createFriend.isPending}
      >
        {createFriend.isPending ? "Saving..." : "Create Friend"}
      </Button>
      {createFriend.error ? <p className="mt-3 text-sm text-red-400">{createFriend.error.message}</p> : null}
    </Card>
  );
}
