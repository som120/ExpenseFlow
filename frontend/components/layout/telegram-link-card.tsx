"use client";

import { useMutation } from "@tanstack/react-query";

import { TelegramLoginButton } from "@/components/auth/telegram-login-button";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { useTelegramLink } from "@/hooks/use-auth";
import { api } from "@/lib/api";
import { useAuthStore } from "@/store/auth-store";

export function TelegramLinkCard() {
  const telegramBotUsername = process.env.NEXT_PUBLIC_TELEGRAM_BOT_USERNAME;
  const telegramLink = useTelegramLink();
  const token = useAuthStore((state) => state.token);
  const manualLink = useMutation({
    mutationFn: async () => {
      if (!token) throw new Error("Login required");
      return api.generateTelegramLinkCode(token);
    },
  });

  if (!telegramBotUsername) {
    return null;
  }

  return (
    <Card>
      <h3 className="text-lg font-semibold">Connect Telegram</h3>
      <p className="mt-2 text-sm text-muted-foreground">
        Link your Telegram account so the website and bot use the same ExpenseFlow profile.
      </p>
      <div className="mt-4">
        <TelegramLoginButton botName={telegramBotUsername} onAuth={(payload) => telegramLink.mutate(payload)} />
      </div>
      <div className="mt-4 rounded-xl border p-4">
        <p className="text-sm font-medium">Manual fallback</p>
        <p className="mt-1 text-sm text-muted-foreground">
          If Telegram login confirmation does not arrive, generate a code and send it to your bot as `/link CODE`.
        </p>
        <Button className="mt-3" variant="secondary" onClick={() => manualLink.mutate()} disabled={!token || manualLink.isPending}>
          {manualLink.isPending ? "Generating..." : "Generate link code"}
        </Button>
        {manualLink.data ? (
          <div className="mt-3 rounded-lg bg-accent p-3 text-sm">
            <p className="font-semibold">Code: {manualLink.data.code}</p>
            <p className="mt-1 text-muted-foreground">{manualLink.data.instructions}</p>
          </div>
        ) : null}
        {manualLink.error ? <p className="mt-3 text-sm text-red-400">{manualLink.error.message}</p> : null}
      </div>
      {telegramLink.isSuccess ? <p className="mt-3 text-sm text-green-400">Telegram linked successfully.</p> : null}
      {telegramLink.error ? <p className="mt-3 text-sm text-red-400">{telegramLink.error.message}</p> : null}
    </Card>
  );
}
