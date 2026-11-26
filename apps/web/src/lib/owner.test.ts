import { beforeEach, describe, expect, it } from "vitest";
import { getOwnerId, ownerHeaders } from "./owner";

describe("owner id", () => {
  beforeEach(() => {
    window.localStorage.clear();
  });

  it("creates an id once and keeps it", () => {
    const first = getOwnerId();
    const second = getOwnerId();

    expect(first).toMatch(/^[0-9a-f-]{36}$/);
    expect(second).toBe(first);
    expect(window.localStorage.getItem("super-prompt-owner-id")).toBe(first);
  });

  it("replaces a stored value that is not a valid id", () => {
    window.localStorage.setItem("super-prompt-owner-id", "hacked");

    expect(getOwnerId()).not.toBe("hacked");
  });

  it("sends the id in the X-Owner-Id header", () => {
    expect(ownerHeaders()["X-Owner-Id"]).toBe(getOwnerId());
  });
});