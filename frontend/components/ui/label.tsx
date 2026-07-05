import * as React from "react";

export function Label({ className, ...props }: React.LabelHTMLAttributes<HTMLLabelElement>) {
  return <label className={className ?? "text-sm font-medium text-foreground"} {...props} />;
}
