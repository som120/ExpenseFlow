"use client";

import { useMutation } from "@tanstack/react-query";

import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { api } from "@/lib/api";
import { useAuthStore } from "@/store/auth-store";

function downloadTextFile(filename: string, content: string, mediaType: string) {
  const blob = new Blob([content], { type: mediaType });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  link.click();
  URL.revokeObjectURL(url);
}

export function ExportButtons() {
  const token = useAuthStore((state) => state.token);

  const csvExport = useMutation({
    mutationFn: async () => {
      const file = await api.exportCsv(token!);
      downloadTextFile(file.filename, file.content, file.media_type);
    },
  });

  const excelExport = useMutation({
    mutationFn: async () => {
      const file = await api.exportExcel(token!);
      downloadTextFile(file.filename, file.content, file.media_type);
    },
  });

  const pdfExport = useMutation({
    mutationFn: async () => {
      const file = await api.exportPdf(token!);
      downloadTextFile(file.filename, file.content, file.media_type);
    },
  });

  return (
    <Card>
      <h3 className="mb-4 text-lg font-semibold">Exports</h3>
      <div className="grid gap-3 md:grid-cols-3">
        <Button onClick={() => csvExport.mutate()} disabled={!token || csvExport.isPending}>Export CSV</Button>
        <Button variant="secondary" onClick={() => excelExport.mutate()} disabled={!token || excelExport.isPending}>Export Excel</Button>
        <Button variant="ghost" onClick={() => pdfExport.mutate()} disabled={!token || pdfExport.isPending}>Export PDF</Button>
      </div>
    </Card>
  );
}
