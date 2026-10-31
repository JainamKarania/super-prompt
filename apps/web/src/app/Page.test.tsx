import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";
import Home from "./page";
import { analyzePrompt } from "@/lib/api";
import { analysisFixture } from "@/test/fixtures";

vi.mock("@/lib/api", () => ({ analyzePrompt: vi.fn() }));

const PLACEHOLDER = "Paste your prompt here...";

describe("Home", () => {
  it("disables Analyze while the prompt is empty", () => {
    render(<Home />);
    expect(screen.getByRole("button", { name: "Analyze" })).toBeDisabled();
  });

  it("enables Analyze once a prompt is typed", async () => {
    const user = userEvent.setup();
    render(<Home />);
    await user.type(screen.getByPlaceholderText(PLACEHOLDER), "Write a blog post");
    expect(screen.getByRole("button", { name: "Analyze" })).toBeEnabled();
  });

  it("shows the score card after analyzing", async () => {
    vi.mocked(analyzePrompt).mockResolvedValue(analysisFixture);
    const user = userEvent.setup();
    render(<Home />);
    await user.type(screen.getByPlaceholderText(PLACEHOLDER), "Write a blog post");
    await user.click(screen.getByRole("button", { name: "Analyze" }));
    expect(await screen.findByText(/Overall score/)).toBeInTheDocument();
  });
});