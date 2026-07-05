import type { LabelHTMLAttributes } from "react";

export function Label({ className, ...props }: LabelHTMLAttributes<HTMLLabelElement>) {
  return <label className={className ?? "text-sm font-medium text-foreground"} {...props} />;
}
