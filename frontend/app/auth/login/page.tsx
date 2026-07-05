"use client";

import { FormEvent, useState } from "react";
import Link from "next/link";

import { useLogin } from "@/hooks/use-auth";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

export default function LoginPage() {
  const login = useLogin();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const onSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    login.mutate({ email, password });
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-background p-6">
      <Card className="w-full max-w-md space-y-6">
        <div>
          <h1 className="text-2xl font-semibold">Welcome back</h1>
          <p className="text-sm text-muted-foreground">Sign in to continue to ExpenseFlow.</p>
        </div>
        <form className="space-y-4" onSubmit={onSubmit}>
          <div>
            <Label>Email</Label>
            <Input type="email" placeholder="you@example.com" value={email} onChange={(e) => setEmail(e.target.value)} />
          </div>
          <div>
            <Label>Password</Label>
            <Input type="password" placeholder="••••••••" value={password} onChange={(e) => setPassword(e.target.value)} />
          </div>
          {login.error ? <p className="text-sm text-red-400">{login.error.message}</p> : null}
          <Button className="w-full" type="submit">{login.isPending ? "Signing in..." : "Sign In"}</Button>
        </form>
        <p className="text-center text-sm text-muted-foreground">
          No account? <Link href="/auth/register" className="text-primary">Create one</Link>
        </p>
      </Card>
    </div>
  );
}
