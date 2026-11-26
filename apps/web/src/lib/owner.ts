const KEY = "super-prompt-owner-id";
const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;

let fallbackId: string | null = null;

/** A random ID that stays the same in this browser. Not a login: it only keeps history private. */
export function getOwnerId(): string {
  try {
    const stored = window.localStorage.getItem(KEY);
    if (stored && UUID.test(stored)) return stored;
    const id = crypto.randomUUID();
    window.localStorage.setItem(KEY, id);
    return id;
  } catch {
    // Storage blocked (private mode, etc.): keep one ID for this page session.
    fallbackId ??= crypto.randomUUID();
    return fallbackId;
  }
}

export function ownerHeaders(): Record<string, string> {
  return { "X-Owner-Id": getOwnerId() };
}