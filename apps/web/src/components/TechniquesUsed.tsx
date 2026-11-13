import type { Technique } from "@/lib/schema";

function isWebUrl(value: string): boolean {
  try {
    const { protocol } = new URL(value);
    return protocol === "http:" || protocol === "https:";
  } catch {
    return false;
  }
}

export function TechniquesUsed({ techniques }: { techniques: Technique[] }) {
  if (techniques.length === 0) return null;

  return (
    <section aria-labelledby="techniques-heading" className="space-y-3">
      <h2 id="techniques-heading" className="text-lg font-semibold">
        Techniques used
      </h2>
      <ul className="space-y-2">
        {techniques.map((t) => (
          <li
            key={t.title}
            className="rounded-lg border p-3 text-sm"
          >
            <p className="font-medium">{t.title}</p>
            {isWebUrl(t.source) ? (
              <a
                href={t.source}
                target="_blank"
                rel="noopener noreferrer"
                className="text-muted-foreground underline underline-offset-4"
              >
                Read the source
              </a>
            ) : null}
          </li>
        ))}
      </ul>
    </section>
  );
}