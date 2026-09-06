import type { Severity } from "@/lib/scan-api";

export const severityStyles: Record<
  Severity,
  { badge: string; text: string; dot: string; bar: string }
> = {
  HIGH: {
    badge: "border-severity-high/40 bg-severity-high-soft text-severity-high",
    text: "text-severity-high",
    dot: "bg-severity-high",
    bar: "bg-severity-high",
  },
  MEDIUM: {
    badge: "border-severity-medium/40 bg-severity-medium-soft text-severity-medium",
    text: "text-severity-medium",
    dot: "bg-severity-medium",
    bar: "bg-severity-medium",
  },
  LOW: {
    badge: "border-severity-low/40 bg-severity-low-soft text-severity-low",
    text: "text-severity-low",
    dot: "bg-severity-low",
    bar: "bg-severity-low",
  },
};

export function SeverityBadgeClass(severity: Severity) {
  return `inline-flex items-center gap-1.5 rounded border px-2 py-0.5 text-[11px] font-semibold uppercase tracking-[0.06em] ${severityStyles[severity].badge}`;
}
