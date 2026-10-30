"use client";

import { useState } from "react";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Skeleton } from "@/components/ui/skeleton";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { ScoreCard } from "@/components/ScoreCard";
import { RewriteView } from "@/components/RewriteView";
import { analyzePrompt } from "@/lib/api";
import { TASK_TYPES, type Analysis, type TaskType } from "@/lib/schema";

export default function Home() {
  const [prompt, setPrompt] = useState("");
  const [task, setTask] = useState<TaskType>("writing");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<Analysis | null>(null);

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    try {
      setResult(await analyzePrompt({ prompt, task }));
    } catch {
      toast.error("Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="mx-auto max-w-4xl space-y-6 p-6">
      <h1 className="text-3xl font-bold">Prompt Coach</h1>

      <form onSubmit={onSubmit} className="space-y-4">
        <Textarea
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Paste your prompt here..."
          rows={6}
        />
        <div className="flex items-center gap-3">
          <Select value={task} onValueChange={(v) => setTask(v as TaskType)}>
            <SelectTrigger className="w-40">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              {TASK_TYPES.map((t) => (
                <SelectItem key={t} value={t} className="capitalize">
                  {t}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
          <Button type="submit" disabled={loading || prompt.trim() === ""}>
            {loading ? "Analyzing..." : "Analyze"}
          </Button>
        </div>
      </form>

      {loading && (
        <div className="space-y-3">
          <Skeleton className="h-40 w-full" />
          <Skeleton className="h-40 w-full" />
        </div>
      )}

      {!loading && result && (
        <div className="space-y-6">
          <ScoreCard analysis={result} />
          <RewriteView analysis={result} />
        </div>
      )}
    </main>
  );
}