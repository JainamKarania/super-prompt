import { afterEach, describe, expect, it, vi } from "vitest";
import { analyzePrompt, getAnalysis, listAnalyses } from "./api";
import { analysisFixture } from "@/test/fixtures";

const json = (body: unknown, status = 200) =>
  new Response(JSON.stringify(body), { status });

afterEach(() => {
  vi.restoreAllMocks();
});

describe("analyzePrompt", () => {
  it("posts the request and parses the response", async () => {
    const fetchMock = vi
      .spyOn(globalThis, "fetch")
      .mockResolvedValue(json(analysisFixture));

    const result = await analyzePrompt({ prompt: "write a blog", task: "writing" });

    expect(result.id).toBe(analysisFixture.id);
    expect(fetchMock).toHaveBeenCalledWith(
      expect.stringContaining("/api/analyze"),
      expect.objectContaining({ method: "POST" }),
    );
  });

  it("throws when the API returns an error", async () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue(json({}, 500));
    await expect(
      analyzePrompt({ prompt: "x", task: "writing" }),
    ).rejects.toThrow();
  });
});

describe("listAnalyses", () => {
  it("returns the parsed list", async () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue(json([analysisFixture]));
    expect(await listAnalyses()).toHaveLength(1);
  });

  it("throws when the API returns an error", async () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue(json({}, 500));
    await expect(listAnalyses()).rejects.toThrow();
  });
});

describe("getAnalysis", () => {
  it("returns the analysis", async () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue(json(analysisFixture));
    expect((await getAnalysis("test-id"))?.id).toBe("test-id");
  });

  it("returns null when the id is not found", async () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue(json({}, 404));
    expect(await getAnalysis("missing")).toBeNull();
  });

  it("throws on a server error", async () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue(json({}, 500));
    await expect(getAnalysis("x")).rejects.toThrow();
  });
});