"use client";

import { useEffect } from "react";

declare global {
  interface Window {
    onTelegramAuth?: (user: Record<string, unknown>) => void;
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
  useEffect(() => {
    window.onTelegramAuth = (user) => {
      onAuth(user as never);
    };

    const script = document.createElement("script");
    script.src = "https://telegram.org/js/telegram-widget.js?22";
    script.async = true;
    script.setAttribute("data-telegram-login", botName);
    script.setAttribute("data-size", "large");
    script.setAttribute("data-userpic", "false");
    script.setAttribute("data-request-access", "write");
    script.setAttribute("data-onauth", "onTelegramAuth(user)");

    const container = document.getElementById("telegram-login-container");
    container?.replaceChildren();
    container?.appendChild(script);

    return () => {
      window.onTelegramAuth = undefined;
    };
  }, [botName, onAuth]);

  return <div id="telegram-login-container" className="flex justify-center" />;
}
