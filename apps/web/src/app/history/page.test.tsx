import { render, screen } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import type { Analysis } from "@/lib/schema";
import HistoryPage from "./page";

const listAnalyses = vi.hoisted(() => vi.fn());
vi.mock("@/lib/api", () => ({ listAnalyses }));

function item(id: string, original: string, overall: number): Analysis {
  return {
    id,
    original,
    overall,
    createdAt: "2026-11-23T10:00:00Z",
  } as unknown as Analysis;
}

describe("HistoryPage", () => {
  beforeEach(() => {
    listAnalyses.mockReset();
  });

  it("lists past analyses with links to their detail pages", async () => {
    listAnalyses.mockResolvedValue([
      item("a1", "Write a blog post about coffee.", 7.5),
      item("b2", "Summarize this report.", 4),
    ]);
    render(<HistoryPage />);

    expect(await screen.findByText("Write a blog post about coffee.")).toBeInTheDocument();
    expect(screen.getByText("7.5 / 10")).toBeInTheDocument();
    expect(screen.getByText("4.0 / 10")).toBeInTheDocument();
    const links = screen.getAllByRole("link");
    expect(links.map((l) => l.getAttribute("href"))).toEqual([
      "/history/a1",
      "/history/b2",
    ]);
  });

  it("shows an empty state that links to the analyzer", async () => {
    listAnalyses.mockResolvedValue([]);
    render(<HistoryPage />);

    const link = await screen.findByRole("link", {
      name: /analyze your first prompt/i,
    });
    expect(link).toHaveAttribute("href", "/analyze");
  });

  it("shows an error message when the API cannot be reached", async () => {
    listAnalyses.mockRejectedValue(new Error("network"));
    render(<HistoryPage />);

    expect(await screen.findByRole("alert")).toHaveTextContent(
      /could not load your history/i,
    );
  });
});
