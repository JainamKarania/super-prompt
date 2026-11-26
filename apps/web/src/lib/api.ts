import { z } from "zod";
import { Analysis, type AnalyzeRequest } from "./schema";
import { ownerHeaders } from "./owner";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export class ApiError extends Error {
  constructor(
    message: string,
    public readonly status: number,
    public readonly retryAfter?: number,
  ) {
    super(message);
    this.name = "ApiError";
  }
}

export function errorMessage(err: unknown): string {
  if (err instanceof ApiError && err.status === 429) {
    return err.retryAfter
      ? `You're going a little fast. Please try again in ${err.retryAfter} seconds.`
      : "You're going a little fast. Please wait a moment and try again.";
  }
  if (err instanceof ApiError && err.status === 502) {
    return "The AI model had a hiccup. Please try again.";
  }
  return "Something went wrong. Please try again.";
}

export async function analyzePrompt(req: AnalyzeRequest): Promise<Analysis> {
  const res = await fetch(`${API_URL}/api/analyze`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...ownerHeaders() },
    body: JSON.stringify(req),
  });
    if (!res.ok) {
    const header = Number(res.headers.get("Retry-After"));
    throw new ApiError(
      `Analyze failed with status ${res.status}`,
      res.status,
      Number.isFinite(header) && header > 0 ? header : undefined,
    );
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