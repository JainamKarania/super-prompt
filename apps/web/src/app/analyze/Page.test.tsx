import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { ApiError } from "@/lib/api";
import type { Analysis } from "@/lib/schema";
import AnalyzePage from "./page";

const analyzePrompt = vi.hoisted(() => vi.fn());

vi.mock("@/lib/api", async (importOriginal) => ({
  ...(await importOriginal<typeof import("@/lib/api")>()),
  analyzePrompt,
}));

const analysis = {
  id: "a1",
  original: "Write a blog post about coffee.",
  improved: "You are a food writer. Write a 600-word blog post about coffee.",
  task: "writing",
  overall: 7.5,
  dimensions: [{ name: "clarity", score: 8, feedback: "Clear goal." }],
  changes: ["Added a role"],
  techniques: [
    { title: "Assign a role", source: "https://example.com/role" },
  ],
  createdAt: "2026-11-23T10:00:00Z",
} as unknown as Analysis;

function typePrompt(text: string) {
  const box = screen.getByPlaceholderText(/paste your prompt here/i);
  fireEvent.change(box, { target: { value: text } });
  return box;
}

describe("AnalyzePage", () => {
  beforeEach(() => {
    analyzePrompt.mockReset();
  });

  it("starts with the submit button disabled", () => {
    render(<AnalyzePage />);

    expect(
      screen.getByRole("heading", { name: /analyze a prompt/i }),
    ).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Analyze" })).toBeDisabled();
  });

  it("counts the characters as you type", () => {
    render(<AnalyzePage />);

    typePrompt("hello");

    expect(screen.getByText(/5 characters/)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Analyze" })).toBeEnabled();
  });

  it("shows the score, the rewrite and the techniques after analyzing", async () => {
    analyzePrompt.mockResolvedValue(analysis);
    render(<AnalyzePage />);

    typePrompt("Write a blog post about coffee.");
    fireEvent.click(screen.getByRole("button", { name: "Analyze" }));

    expect(await screen.findByText(/overall score: 7\.5 \/ 10/i)).toBeInTheDocument();
    expect(screen.getByText("Improved")).toBeInTheDocument();
    expect(screen.getByText("Techniques used")).toBeInTheDocument();
    expect(analyzePrompt).toHaveBeenCalledWith({
      prompt: "Write a blog post about coffee.",
      task: "writing",
    });
  });

  it("shows a friendly message when rate limited", async () => {
    analyzePrompt.mockRejectedValue(new ApiError("limited", 429, 30));
    vi.spyOn(console, "error").mockImplementation(() => {});
    render(<AnalyzePage />);

    typePrompt("Write a blog post about coffee.");
    fireEvent.click(screen.getByRole("button", { name: "Analyze" }));

    expect(await screen.findByRole("alert")).toHaveTextContent("30 seconds");
  });

  it("clears an old error when you try again", async () => {
    analyzePrompt.mockRejectedValueOnce(new ApiError("bad", 502));
    analyzePrompt.mockResolvedValueOnce(analysis);
    vi.spyOn(console, "error").mockImplementation(() => {});
    render(<AnalyzePage />);

    typePrompt("Write a blog post about coffee.");
    fireEvent.click(screen.getByRole("button", { name: "Analyze" }));
    expect(await screen.findByRole("alert")).toBeInTheDocument();

    fireEvent.click(screen.getByRole("button", { name: "Analyze" }));

    await screen.findByText(/overall score/i);
    expect(screen.queryByRole("alert")).not.toBeInTheDocument();
  });

  it("submits with Ctrl+Enter", async () => {
    analyzePrompt.mockResolvedValue(analysis);
    render(<AnalyzePage />);

    const box = typePrompt("Write a blog post about coffee.");
    fireEvent.keyDown(box, { key: "Enter", ctrlKey: true });

    await waitFor(() => expect(analyzePrompt).toHaveBeenCalledTimes(1));
  });

  it("ignores Ctrl+Enter when the prompt is empty", () => {
    render(<AnalyzePage />);

    const box = screen.getByPlaceholderText(/paste your prompt here/i);
    fireEvent.keyDown(box, { key: "Enter", ctrlKey: true });

    expect(analyzePrompt).not.toHaveBeenCalled();
  });
});
