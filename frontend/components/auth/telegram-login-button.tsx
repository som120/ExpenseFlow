"use client";

import Script from "next/script";
import { useEffect, useId, useState } from "react";

declare global {
  interface Window {
    onTelegramAuth?: (user: Record<string, unknown>) => void;
    [key: string]: unknown;
  }
}

interface TelegramLoginButtonProps {
  botName: string;
  onAuth: (payload: {
    id: number;
    first_name: string;
    last_name?: string;
    username?: string;
    photo_url?: string;
    auth_date: number;
    hash: string;
  }) => void;
}

export function TelegramLoginButton({ botName, onAuth }: TelegramLoginButtonProps) {
  const [mounted, setMounted] = useState(false);
  const callbackName = `onTelegramAuth_${useId().replace(/[^a-zA-Z0-9_]/g, "_")}`;

  useEffect(() => {
    setMounted(true);
  }, []);

  useEffect(() => {
    if (!mounted) {
      return;
    }

    window[callbackName as keyof Window] = ((user: Record<string, unknown>) => {
      onAuth(user as never);
    }) as never;

    return () => {
      delete window[callbackName as keyof Window];
    };
  }, [callbackName, mounted, onAuth]);

  if (!mounted) {
    return <div className="flex justify-center" />;
  }

  return (
    <div className="flex justify-center">
      <Script
        id={`telegram-login-${callbackName}`}
        src="https://telegram.org/js/telegram-widget.js?22"
        strategy="afterInteractive"
        data-telegram-login={botName}
        data-size="large"
        data-userpic="false"
        data-request-access="write"
        data-onauth={`${callbackName}(user)`}
      />
    </div>
  );
}
