"use client";

import { TelegramLoginButton } from "@/components/auth/telegram-login-button";
import { Card } from "@/components/ui/card";
import { useTelegramLink } from "@/hooks/use-auth";

export function TelegramLinkCard() {
  const telegramBotUsername = process.env.NEXT_PUBLIC_TELEGRAM_BOT_USERNAME;
  const telegramLink = useTelegramLink();

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
      {telegramLink.isSuccess ? <p className="mt-3 text-sm text-green-400">Telegram linked successfully.</p> : null}
      {telegramLink.error ? <p className="mt-3 text-sm text-red-400">{telegramLink.error.message}</p> : null}
    </Card>
  );
}
