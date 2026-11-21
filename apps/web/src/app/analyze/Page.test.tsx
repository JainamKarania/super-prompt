import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import Home from "../page";

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