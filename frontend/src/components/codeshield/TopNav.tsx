import { Github, ShieldCheck } from "lucide-react";

const NAV_ITEMS = [
  { label: "Dashboard", href: "#dashboard" },
  { label: "Scanner", href: "#scanner" },
  { label: "Reports", href: "#results" },
];

export function TopNav() {
  return (
    <header className="sticky top-0 z-40 border-b border-border bg-card/95 backdrop-blur-[2px]">
      <div className="mx-auto flex h-16 max-w-[1400px] items-center justify-between gap-4 px-4 sm:px-6">
        <div className="flex items-center gap-3">
          <div className="flex h-9 w-9 items-center justify-center rounded-md border border-border bg-secondary">
            <ShieldCheck className="h-5 w-5 text-primary" aria-hidden="true" />
          </div>
          <div className="leading-tight">
            <div className="text-[15px] font-semibold tracking-tight text-foreground">
              CodeShield
            </div>
            <div className="hidden text-[11px] uppercase tracking-[0.08em] text-muted-foreground sm:block">
              Vulnerability Detection Platform
            </div>
          </div>
        </div>

        <nav className="flex items-center gap-1">
          {NAV_ITEMS.map((item) => (
            <a
              key={item.label}
              href={item.href}
              className="rounded-md px-3 py-1.5 text-sm text-muted-foreground transition-colors hover:bg-secondary hover:text-foreground"
            >
              {item.label}
            </a>
          ))}
          <a
            href="https://github.com"
            target="_blank"
            rel="noreferrer"
            aria-label="Open project repository on GitHub"
            className="ml-2 flex h-8 w-8 items-center justify-center rounded-md border border-border text-muted-foreground transition-colors hover:bg-secondary hover:text-foreground"
          >
            <Github className="h-4 w-4" aria-hidden="true" />
          </a>
        </nav>
      </div>
    </header>
  );
}
