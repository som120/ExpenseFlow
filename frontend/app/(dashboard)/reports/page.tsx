"use client";

import { ExportButtons } from "@/components/reports/export-buttons";
import { ReportCard } from "@/components/reports/report-card";
import { useReportsQuery } from "@/hooks/use-dashboard-data";

export default function ReportsPage() {
  const { data } = useReportsQuery();

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-semibold">Reports</h2>
        <p className="text-sm text-muted-foreground">Generate summaries and download finance exports.</p>
      </div>
      <ReportCard report={data} />
      <ExportButtons />
    </div>
  );
}
