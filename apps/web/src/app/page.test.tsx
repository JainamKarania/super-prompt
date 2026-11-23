import { render, screen } from "@testing-library/react";
import { afterAll, beforeAll, describe, expect, it, vi } from "vitest";
import Home from "./page";

beforeAll(() => {
  vi.stubGlobal(
    "IntersectionObserver",
    class {
      observe() {}
      unobserve() {}
      disconnect() {}
      takeRecords() {
        return [];
      }
    },
  );
});

afterAll(() => {
  vi.unstubAllGlobals();
});

describe("Home", () => {
  it("explains the product and links to the analyzer", () => {
    render(<Home />);

    expect(screen.getByRole("heading", { level: 1 })).toHaveTextContent(
      /better prompts/i,
    );
    const ctas = screen.getAllByRole("link", { name: /analyze a prompt/i });
    expect(ctas.length).toBeGreaterThan(0);
    for (const cta of ctas) {
      expect(cta).toHaveAttribute("href", "/analyze");
    }
  });

  it("shows the three steps", () => {
    render(<Home />);

    expect(screen.getByText("Score it")).toBeInTheDocument();
    expect(screen.getByText("Rewrite it")).toBeInTheDocument();
    expect(screen.getByText("Learn why")).toBeInTheDocument();
  });
});
