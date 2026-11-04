import Link from "next/link";

export function SiteHeader() {
  return (
    <header className="border-b">
      <nav className="mx-auto flex max-w-4xl items-center gap-6 p-4 text-sm font-medium">
        <Link href="/" className="font-bold">
          Super Prompt
        </Link>
        <Link href="/" className="text-muted-foreground hover:text-foreground">
          Analyze
        </Link>
        <Link
          href="/history"
          className="text-muted-foreground hover:text-foreground"
        >
          Prompt History
        </Link>
      </nav>
    </header>
  );
}