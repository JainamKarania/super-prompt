"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { Skeleton } from "@/components/ui/skeleton";
import { ScoreCard } from "@/components/ScoreCard";
import { RewriteView } from "@/components/RewriteView";
import { getAnalysis } from "@/lib/api";
import type { Analysis } from "@/lib/schema";
import { TechniquesUsed } from "@/components/TechniquesUsed";

export default function HistoryDetailPage() {
  const { id } = useParams<{ id: string }>();
  const [analysis, setAnalysis] = useState<Analysis | null | undefined>(
    undefined,
  );
  const [failed, setFailed] = useState(false);

useEffect(() => {
  getAnalysis(id)
    .then(setAnalysis)
    .catch(() => setFailed(true));
}, [id]);

  useEffect(() => {
    getAnalysis(id).then(setAnalysis);
  }, [id]);

  return (
    <main className="mx-auto max-w-4xl space-y-6 p-6">
      <Link href="/history" className="text-sm text-muted-foreground underline">
        Back to history
      </Link>

      {analysis === undefined && <Skeleton className="h-40 w-full" />}

      {failed && (
  <p className="text-destructive">
    Could not load this analysis. Is the API running?
  </p>
)}

      {analysis === null && <p>That analysis was not found.</p>}

      {analysis && (
        <>
          <ScoreCard analysis={analysis} />
          <RewriteView analysis={analysis} />
          <TechniquesUsed techniques={analysis.techniques} />
        </>
      )}
    </main>
  );
}