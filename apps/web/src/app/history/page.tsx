"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { listAnalyses } from "@/lib/api";
import type { Analysis } from "@/lib/schema";

export default function HistoryPage() {
  const [items, setItems] = useState<Analysis[] | null>(null);
  const [failed, setFailed] = useState(false);

useEffect(() => {
  listAnalyses()
    .then(setItems)
    .catch(() => setFailed(true));
}, []);

  useEffect(() => {
    listAnalyses().then(setItems);
  }, []);

  return (
    <main className="mx-auto max-w-4xl space-y-4 p-6">
      <h1 className="text-3xl font-bold">History</h1>

      {items === null && <Skeleton className="h-24 w-full" />}

      {failed && (
  <p className="text-destructive">
    Could not load history. Is the API running?
  </p>
      )}

      {items?.length === 0 && (
        <p className="text-muted-foreground">
          No analyses yet.{" "}
          <Link href="/" className="underline">
            Analyze your first prompt
          </Link>
          .
        </p>
      )}

      {items?.map((a) => (
        <Link key={a.id} href={`/history/${a.id}`} className="block">
          <Card className="transition-colors hover:bg-muted/50">
            <CardContent className="flex items-start justify-between gap-4 pt-6">
              <div className="min-w-0">
                <p className="line-clamp-2 text-sm">{a.original}</p>
                <p className="mt-1 text-xs text-muted-foreground">
                  {new Date(a.createdAt).toLocaleString()}
                </p>
              </div>
              <Badge>{a.overall.toFixed(1)} / 10</Badge>
            </CardContent>
          </Card>
        </Link>
      ))}
    </main>
  );
}