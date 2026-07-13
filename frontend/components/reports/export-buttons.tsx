"use client";

import { useMutation } from "@tanstack/react-query";

import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { api } from "@/lib/api";
import { useAuthStore } from "@/store/auth-store";

function base64ToUint8Array(content: string) {
  const binary = atob(content);
  const bytes = new Uint8Array(binary.length);
  for (let index = 0; index < binary.length; index += 1) {
    bytes[index] = binary.charCodeAt(index);
  }
  return bytes;
}

function downloadFile(filename: string, content: string, mediaType: string, encoding: string) {
  const blob = new Blob(
    [encoding === "base64" ? base64ToUint8Array(content) : content],
    { type: mediaType },
  );
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
      downloadFile(file.filename, file.content, file.media_type, file.encoding);
    },
  });

  const excelExport = useMutation({
    mutationFn: async () => {
      const file = await api.exportExcel(token!);
      downloadFile(file.filename, file.content, file.media_type, file.encoding);
    },
  });

  const pdfExport = useMutation({
    mutationFn: async () => {
      const file = await api.exportPdf(token!);
      downloadFile(file.filename, file.content, file.media_type, file.encoding);
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
