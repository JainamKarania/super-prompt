"use client";

import { useState } from "react";
import { Reveal } from "@/components/motion";
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
import { analyzePrompt, errorMessage } from "@/lib/api";
import { TASK_TYPES, type Analysis, type TaskType } from "@/lib/schema";
import { TechniquesUsed } from "@/components/TechniquesUsed";

export default function AnalyzePage() {
  const [prompt, setPrompt] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [task, setTask] = useState<TaskType>("writing");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<Analysis | null>(null);

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setResult(null);
    setLoading(true);
    try {
      setResult(await analyzePrompt({ prompt, task }));
    } catch (err) {
      setError(errorMessage(err));
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  function onPromptKeyDown(e: React.KeyboardEvent<HTMLTextAreaElement>) {
    if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) {
      e.preventDefault();
      if (!loading && prompt.trim() !== "") {
        e.currentTarget.form?.requestSubmit();
      }
    }
  }

  return (
    <main className="mx-auto max-w-4xl space-y-6 p-6">
      <h1 className="text-3xl font-bold">Analyze a prompt</h1>

      <form onSubmit={onSubmit} className="space-y-4">
        <div className="space-y-1">
          <Textarea
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            onKeyDown={onPromptKeyDown}
            placeholder="Paste your prompt here..."
            rows={6}
          />
          <p className="text-xs text-muted-foreground">
            {prompt.length} characters · Ctrl+Enter to submit
          </p>
        </div>
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

      {error ? (
        <p role="alert" className="text-sm text-destructive">
          {error}
        </p>
      ) : null}

      {loading && (
        <div className="space-y-3">
          <Skeleton className="h-40 w-full" />
          <Skeleton className="h-40 w-full" />
        </div>
      )}

      {!loading && result && (
        <div className="space-y-6">
          <Reveal>
            <ScoreCard analysis={result} />
          </Reveal>
          <Reveal delay={0.15}>
            <RewriteView analysis={result} />
          </Reveal>
          <Reveal delay={0.3}>
            <TechniquesUsed techniques={result.techniques} />
          </Reveal>
        </div>
      )}
    </main>
  );
}
