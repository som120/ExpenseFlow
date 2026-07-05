"use client";

import { FormEvent, useState } from "react";
import Link from "next/link";

import { useRegister } from "@/hooks/use-auth";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

export default function RegisterPage() {
  const register = useRegister();
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const onSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    register.mutate({ full_name: fullName, email, password });
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-background p-6">
      <Card className="w-full max-w-md space-y-6">
        <div>
          <h1 className="text-2xl font-semibold">Create your account</h1>
          <p className="text-sm text-muted-foreground">Track expenses, split bills, and manage budgets.</p>
        </div>
        <form className="space-y-4" onSubmit={onSubmit}>
          <div>
            <Label>Full name</Label>
            <Input placeholder="ExpenseFlow User" value={fullName} onChange={(e) => setFullName(e.target.value)} />
          </div>
          <div>
            <Label>Email</Label>
            <Input type="email" placeholder="you@example.com" value={email} onChange={(e) => setEmail(e.target.value)} />
          </div>
          <div>
            <Label>Password</Label>
            <Input type="password" placeholder="••••••••" value={password} onChange={(e) => setPassword(e.target.value)} />
          </div>
          {register.error ? <p className="text-sm text-red-400">{register.error.message}</p> : null}
          <Button className="w-full" type="submit">{register.isPending ? "Creating..." : "Create Account"}</Button>
        </form>
        <p className="text-center text-sm text-muted-foreground">
          Already have an account? <Link href="/auth/login" className="text-primary">Sign in</Link>
        </p>
      </Card>
    </div>
  );
}
