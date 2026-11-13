import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { TechniquesUsed } from "./TechniquesUsed";

describe("TechniquesUsed", () => {
  it("renders nothing when there are no techniques", () => {
    const { container } = render(<TechniquesUsed techniques={[]} />);
    expect(container).toBeEmptyDOMElement();
  });

  it("shows each technique with a safe link", () => {
    render(
      <TechniquesUsed
        techniques={[
          { title: "Specify the output format", source: "https://example.com/format" },
        ]}
      />,
    );
    expect(screen.getByText("Specify the output format")).toBeInTheDocument();
    const link = screen.getByRole("link", { name: "Read the source" });
    expect(link).toHaveAttribute("href", "https://example.com/format");
    expect(link).toHaveAttribute("rel", "noopener noreferrer");
  });

  it("does not link a source that is not http(s)", () => {
    render(
      <TechniquesUsed
        techniques={[{ title: "Odd one", source: "javascript:alert(1)" }]}
      />,
    );
    expect(screen.getByText("Odd one")).toBeInTheDocument();
    expect(screen.queryByRole("link")).not.toBeInTheDocument();
  });
});