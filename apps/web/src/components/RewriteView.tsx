"use client";

import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import type { Analysis } from "@/lib/schema";

export function RewriteView({ analysis }: { analysis: Analysis }) {
  async function copy() {
    await navigator.clipboard.writeText(analysis.improved);
    toast.success("Improved prompt copied");
  }

  return (
    <div className="grid gap-4 md:grid-cols-2">
      <Card>
        <CardHeader>
          <CardTitle>Original</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="whitespace-pre-wrap text-sm">{analysis.original}</p>
        </CardContent>
      </Card>
      <Card>
        <CardHeader className="flex flex-row items-center justify-between">
          <CardTitle>Improved</CardTitle>
          <Button size="sm" variant="outline" onClick={copy}>
            Copy
          </Button>
        </CardHeader>
        <CardContent className="space-y-3">
          <p className="whitespace-pre-wrap text-sm">{analysis.improved}</p>
          <ul className="list-disc pl-5 text-sm text-muted-foreground">
            {analysis.changes.map((c) => (
              <li key={c}>{c}</li>
            ))}
          </ul>
        </CardContent>
      </Card>
    </div>
  );
}