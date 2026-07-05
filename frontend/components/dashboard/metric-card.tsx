import { Card } from "@/components/ui/card";

export function MetricCard({ label, value, helper }: { label: string; value: string; helper?: string }) {
  return (
    <Card>
      <p className="text-sm text-muted-foreground">{label}</p>
      <p className="mt-3 text-3xl font-semibold">{value}</p>
      {helper ? <p className="mt-2 text-xs text-muted-foreground">{helper}</p> : null}
    </Card>
  );
}
