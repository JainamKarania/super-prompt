import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { ScoreCard } from "./ScoreCard";
import { DIMENSION_NAMES } from "@/lib/schema";
import { analysisFixture } from "@/test/fixtures";

describe("ScoreCard", () => {
  it("shows the overall score", () => {
    render(<ScoreCard analysis={analysisFixture} />);
    expect(screen.getByText("Overall score: 3.0 / 10")).toBeInTheDocument();
  });

  it("renders every dimension with its feedback", () => {
    render(<ScoreCard analysis={analysisFixture} />);
    for (const name of DIMENSION_NAMES) {
      expect(screen.getByText(name)).toBeInTheDocument();
      expect(screen.getByText(`${name} feedback`)).toBeInTheDocument();
    }
  });
});