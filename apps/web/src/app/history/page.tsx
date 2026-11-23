"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { Reveal } from "@/components/motion";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { listAnalyses } from "@/lib/api";
import type { Analysis } from "@/lib/schema";

export default function HistoryPage() {
  const [items, setItems] = useState<Analysis[] | null>(null);
  const [failed, setFailed] = useState(false);

  useEffect(() => {
    let cancelled = false;
    listAnalyses()
      .then((result) => {
        if (!cancelled) setItems(result);
      })
      .catch(() => {
        if (!cancelled) setFailed(true);
      });
    return () => {
      cancelled = true;
    };
  }, []);

  return (
    <main className="mx-auto max-w-4xl space-y-4 p-6">
      <h1 className="text-3xl font-bold">History</h1>

      {items === null && !failed && <Skeleton className="h-24 w-full" />}

      {failed && (
        <p role="alert" className="text-destructive">
          Could not load your history. Is the API running?
        </p>
      )}

      {items?.length === 0 && (
        <p className="text-muted-foreground">
          No analyses yet.{" "}
          <Link href="/analyze" className="underline">
            Analyze your first prompt
          </Link>
          .
        </p>
      )}

      {items?.map((a, index) => (
        <Reveal key={a.id} delay={Math.min(index * 0.05, 0.4)}>
          <Link href={`/history/${a.id}`} className="block">
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
        </Reveal>
      ))}
    </main>
  );
}
