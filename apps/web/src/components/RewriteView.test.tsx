import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import type { Analysis } from "@/lib/schema";
import { RewriteView } from "./RewriteView";

const toast = vi.hoisted(() => ({ success: vi.fn(), error: vi.fn() }));
vi.mock("sonner", () => ({ toast }));

const analysis = {
  original: "Write a blog post.",
  improved: "You are a food writer. Write a 600-word blog post.",
  changes: ["Added a role"],
} as unknown as Analysis;

function mockClipboard(writeText: () => Promise<void>) {
  Object.defineProperty(navigator, "clipboard", {
    value: { writeText },
    configurable: true,
  });
}

describe("RewriteView copy button", () => {
  beforeEach(() => {
    toast.success.mockClear();
    toast.error.mockClear();
  });

  it("copies the improved prompt and confirms with a toast", async () => {
    const writeText = vi.fn().mockResolvedValue(undefined);
    mockClipboard(writeText);
    render(<RewriteView analysis={analysis} />);

    fireEvent.click(screen.getByRole("button", { name: "Copy" }));

    await waitFor(() =>
      expect(toast.success).toHaveBeenCalledWith("Improved prompt copied"),
    );
    expect(writeText).toHaveBeenCalledWith(analysis.improved);
  });

  it("shows an error toast when copying fails", async () => {
    mockClipboard(vi.fn().mockRejectedValue(new Error("denied")));
    render(<RewriteView analysis={analysis} />);

    fireEvent.click(screen.getByRole("button", { name: "Copy" }));

    await waitFor(() => expect(toast.error).toHaveBeenCalled());
    expect(toast.success).not.toHaveBeenCalled();
  });
});
