import type { HTMLAttributes } from "react";

import { cn } from "@/lib/utils";

export function Badge({ className, ...props }: HTMLAttributes<HTMLSpanElement>) {
  return (
    <span
      className={cn("inline-flex rounded-full bg-accent px-2.5 py-1 text-xs text-accent-foreground", className)}
      {...props}
    />
  );
}
