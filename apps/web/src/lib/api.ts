import { Analysis, type AnalyzeRequest } from "./schema";

export async function analyzePrompt(req: AnalyzeRequest): Promise<Analysis> {
  await new Promise((resolve) => setTimeout(resolve, 900)); // fake latency

  const dimensions = [
    { name: "clarity", score: 6, feedback: "The goal is understandable but could be more specific." },
    { name: "context", score: 3, feedback: "No background on the audience or purpose." },
    { name: "constraints", score: 4, feedback: "No limits on length, tone, or scope." },
    { name: "format", score: 2, feedback: "The desired output format is not stated." },
    { name: "examples", score: 1, feedback: "No example of what a good answer looks like." },
  ];
  const overall =
    dimensions.reduce((sum, d) => sum + d.score, 0) / dimensions.length;

  return Analysis.parse({
    id: crypto.randomUUID(),
    original: req.prompt,
    improved:
      `You are helping with a ${req.task} task.\n\n` +
      `Task: ${req.prompt}\n\n` +
      `Audience and purpose: [describe who this is for and why]\n` +
      `Constraints: [length, tone, scope]\n` +
      `Output format: [bullets, table, JSON, etc.]\n` +
      `Example of a good answer: [paste one]`,
    overall,
    dimensions,
    changes: [
      "Added a role and a task type",
      "Added placeholders for audience, constraints, and format",
      "Added a slot for an example answer",
    ],
  });
}