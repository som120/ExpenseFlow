"use client";

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
  const [scriptLoaded, setScriptLoaded] = useState(false);
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

  useEffect(() => {
    if (!mounted) {
      return;
    }

    const existingScript = document.querySelector('script[src="https://telegram.org/js/telegram-widget.js?22"]');
    if (existingScript) {
      setScriptLoaded(true);
      return;
    }

    const script = document.createElement("script");
    script.src = "https://telegram.org/js/telegram-widget.js?22";
    script.async = true;
    script.onload = () => setScriptLoaded(true);
    document.body.appendChild(script);

    return () => {
      script.remove();
    };
  }, [mounted]);

  useEffect(() => {
    if (!scriptLoaded) {
      return;
    }

    const container = document.getElementById(`telegram-login-container-${callbackName}`);
    if (!container) {
      return;
    }

    container.replaceChildren();

    const widgetScript = document.createElement("script");
    widgetScript.src = "https://telegram.org/js/telegram-widget.js?22";
    widgetScript.async = true;
    widgetScript.setAttribute("data-telegram-login", botName);
    widgetScript.setAttribute("data-size", "large");
    widgetScript.setAttribute("data-userpic", "false");
    widgetScript.setAttribute("data-request-access", "write");
    widgetScript.setAttribute("data-onauth", `${callbackName}(user)`);

    container.appendChild(widgetScript);
  }, [botName, callbackName, scriptLoaded]);

  if (!mounted) {
    return <div className="flex justify-center" />;
  }

  return <div id={`telegram-login-container-${callbackName}`} className="flex justify-center" />;
}
