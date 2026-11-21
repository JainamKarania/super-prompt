"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";

const links = [
  { href: "/analyze", label: "Analyze" },
  { href: "/history", label: "History" },
];

export function SiteHeader() {
  const pathname = usePathname();

  return (
    <header className="border-b">
      <nav
        aria-label="Main"
        className="mx-auto flex max-w-4xl items-center gap-6 p-4 text-sm font-medium"
      >
        <Link href="/" className="text-base font-bold">
          super-prompt
        </Link>
        <div className="flex items-center gap-4">
          {links.map(({ href, label }) => {
            const active = pathname === href || pathname.startsWith(`${href}/`);
            return (
              <Link
                key={href}
                href={href}
                aria-current={active ? "page" : undefined}
                className={cn(
                  "hover:text-foreground",
                  active ? "text-foreground" : "text-muted-foreground",
                )}
              >
                {label}
              </Link>
            );
          })}
        </div>
      </nav>
    </header>
  );
}