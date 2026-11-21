import { render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { SiteHeader } from "./SiteHeader";

vi.mock("next/navigation", () => ({ usePathname: () => "/history/abc" }));

describe("SiteHeader", () => {
  it("marks the current section as active", () => {
    render(<SiteHeader />);

    expect(screen.getByRole("link", { name: "History" })).toHaveAttribute(
      "aria-current",
      "page",
    );
    expect(screen.getByRole("link", { name: "Analyze" })).not.toHaveAttribute(
      "aria-current",
    );
  });

  it("links the brand to the home page", () => {
    render(<SiteHeader />);

    expect(screen.getByRole("link", { name: "super-prompt" })).toHaveAttribute(
      "href",
      "/",
    );
  });
});