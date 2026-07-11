import { Card } from "@/components/ui/card";
import type { Report } from "@/types";

export function ReportCard({ report }: { report: Report | undefined }) {
  return (
    <Card>
      <div className="mb-4">
        <h3 className="text-lg font-semibold">Latest Report</h3>
        <p className="text-sm text-muted-foreground">Generated summary for exports and reporting.</p>
      </div>
      <div className="space-y-3">
        {report?.sections.map((section) => (
          <div key={section.title} className="flex items-center justify-between rounded-xl border p-3 text-sm">
            <span>{section.title}</span>
            <span>{section.value}</span>
          </div>
        ))}
      </div>
    </Card>
  );
}
