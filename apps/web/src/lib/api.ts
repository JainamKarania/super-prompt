import { z } from "zod";
import { Analysis, type AnalyzeRequest } from "./schema";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export async function analyzePrompt(req: AnalyzeRequest): Promise<Analysis> {
  const res = await fetch(`${API_URL}/api/analyze`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(req),
  });
  if (!res.ok) {
    throw new Error(`Analyze failed with status ${res.status}`);
  }
  return Analysis.parse(await res.json());
}

export async function listAnalyses(): Promise<Analysis[]> {
  const res = await fetch(`${API_URL}/api/analyses`);
  if (!res.ok) {
    throw new Error(`List failed with status ${res.status}`);
  }
  return z.array(Analysis).parse(await res.json());
}

export async function getAnalysis(id: string): Promise<Analysis | null> {
  const res = await fetch(`${API_URL}/api/analyses/${encodeURIComponent(id)}`);
  if (res.status === 404 || res.status === 422) return null;
  if (!res.ok) {
    throw new Error(`Fetch failed with status ${res.status}`);
  }
  return Analysis.parse(await res.json());
}