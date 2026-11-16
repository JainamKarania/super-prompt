import { afterEach, describe, expect, it, vi } from "vitest";
import { analyzePrompt, ApiError, errorMessage } from "./api";

afterEach(() => {
  vi.unstubAllGlobals();
});

describe("rate limit handling", () => {
  it("throws an ApiError carrying Retry-After on a 429", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(
        new Response("{}", { status: 429, headers: { "Retry-After": "42" } }),
      ),
    );

    const err = await analyzePrompt({
      prompt: "Write a blog post about rate limits",
      task: "writing",
    }).catch((e: unknown) => e);

    expect(err).toBeInstanceOf(ApiError);
    expect((err as ApiError).status).toBe(429);
    expect((err as ApiError).retryAfter).toBe(42);
  });

  it("shows the wait time in the message", () => {
    expect(errorMessage(new ApiError("x", 429, 42))).toContain("42 seconds");
  });

  it("falls back to a generic message when there is no wait time", () => {
    expect(errorMessage(new ApiError("x", 429))).toContain("wait a moment");
  });

  it("uses a safe default for unknown errors", () => {
    expect(errorMessage(new Error("boom"))).toBe(
      "Something went wrong. Please try again.",
    );
  });
});