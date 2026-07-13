"use client";

import { useState } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";

import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { api } from "@/lib/api";
import { useAuthStore } from "@/store/auth-store";

export function ReceiptUploadCard() {
  const token = useAuthStore((state) => state.token);
  const queryClient = useQueryClient();
  const [file, setFile] = useState<File | null>(null);

  const uploadMutation = useMutation({
    mutationFn: () => api.uploadReceipt(token!, file!),
    onSuccess: () => {
      setFile(null);
      queryClient.invalidateQueries({ queryKey: ["transactions"] });
      queryClient.invalidateQueries({ queryKey: ["summary"] });
      queryClient.invalidateQueries({ queryKey: ["analytics"] });
    },
  });

  return (
    <Card>
      <div className="mb-4">
        <h3 className="text-lg font-semibold">Upload Receipt</h3>
        <p className="text-sm text-muted-foreground">Upload a bill image to extract OCR text and save it as a transaction.</p>
      </div>
      <input
        type="file"
        accept="image/*"
        onChange={(event) => setFile(event.target.files?.[0] ?? null)}
        className="block w-full text-sm text-muted-foreground"
      />
      <Button className="mt-4" onClick={() => uploadMutation.mutate()} disabled={!token || !file || uploadMutation.isPending}>
        {uploadMutation.isPending ? "Processing..." : "Upload Receipt"}
      </Button>
      {uploadMutation.data ? (
        <div className="mt-4 rounded-xl border p-3 text-sm">
          <p className="font-medium">{uploadMutation.data.message}</p>
          <pre className="mt-2 whitespace-pre-wrap text-xs text-muted-foreground">{uploadMutation.data.extracted_text}</pre>
        </div>
      ) : null}
      {uploadMutation.error ? <p className="mt-3 text-sm text-red-400">{uploadMutation.error.message}</p> : null}
    </Card>
  );
}
