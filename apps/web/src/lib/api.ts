import { z } from "zod";
import { Analysis, type AnalyzeRequest } from "./schema";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
const STORAGE_KEY = "prompt-coach-history";

function readHistory(): Analysis[] {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? z.array(Analysis).parse(JSON.parse(raw)) : [];
  } catch {
    return [];
  }
}

function saveToHistory(item: Analysis) {
  try {
    const next = [item, ...readHistory()];
    localStorage.setItem(STORAGE_KEY, JSON.stringify(next));
  } catch {
    // storage unavailable: history just won't persist
  }
}

export async function analyzePrompt(req: AnalyzeRequest): Promise<Analysis> {
  const res = await fetch(`${API_URL}/api/analyze`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(req),
  });
  if (!res.ok) {
    throw new Error(`Analyze failed with status ${res.status}`);
  }
  const result = Analysis.parse(await res.json());
  saveToHistory(result);
  return result;
}

export async function listAnalyses(): Promise<Analysis[]> {
  return readHistory();
}

export async function getAnalysis(id: string): Promise<Analysis | null> {
  return readHistory().find((a) => a.id === id) ?? null;
}