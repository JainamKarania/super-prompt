import { z } from "zod";

export const TASK_TYPES = ["writing", "code", "analysis"] as const;
export const DIMENSION_NAMES = [
  "clarity",
  "context",
  "constraints",
  "format",
  "examples",
] as const;

export const AnalyzeRequest = z.object({
  prompt: z.string().min(1, "Enter a prompt"),
  task: z.enum(TASK_TYPES),
});
export type AnalyzeRequest = z.infer<typeof AnalyzeRequest>;
export type TaskType = (typeof TASK_TYPES)[number];

export const Dimension = z.object({
  name: z.enum(DIMENSION_NAMES),
  score: z.number().min(0).max(10),
  feedback: z.string(),
});

export const Analysis = z.object({
  id: z.string(),
  original: z.string(),
  improved: z.string(),
  overall: z.number().min(0).max(10),
  dimensions: z.array(Dimension),
  changes: z.array(z.string()),
});
export type Analysis = z.infer<typeof Analysis>;