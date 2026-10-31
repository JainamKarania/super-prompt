import { DIMENSION_NAMES, type Analysis } from "@/lib/schema";

export const analysisFixture: Analysis = {
  id: "test-id",
  createdAt: new Date("2026-10-31T00:00:00.000Z"),
  original: "write a blog",
  improved: "You are helping with a writing task.",
  overall: 3,
  dimensions: DIMENSION_NAMES.map((name, i) => ({
    name,
    score: i + 1,
    feedback: `${name} feedback`,
  })),
  changes: ["Added a role"],
};