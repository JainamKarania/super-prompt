import { render, screen, waitFor } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import type { Analysis } from "@/lib/schema";
import { ScoreCard } from "./ScoreCard";

// Replace the shadcn bar with a plain one that exposes its value, so this test
// checks our animation logic and not the internals of the UI library.
vi.mock("@/components/ui/progress", () => ({
  Progress: ({ value }: { value: number }) => (
    <div role="progressbar" data-value={value} />
  ),
}));

const analysis = {
  overall: 6.5,
  dimensions: [
    { name: "clarity", score: 8, feedback: "Clear goal." },
    { name: "context", score: 3, feedback: "Add background." },
  ],
} as unknown as Analysis;

describe("ScoreCard progress bars", () => {
  it("shows the overall score right away", () => {
    render(<ScoreCard analysis={analysis} />);

    expect(screen.getByText("Overall score: 6.5 / 10")).toBeInTheDocument();
  });

  it("fills each bar to its score after the animation starts", async () => {
    render(<ScoreCard analysis={analysis} />);

    await waitFor(() => {
      const values = screen
        .getAllByRole("progressbar")
        .map((bar) => bar.getAttribute("data-value"));
      expect(values).toEqual(["80", "30"]);
    });
  });
});
