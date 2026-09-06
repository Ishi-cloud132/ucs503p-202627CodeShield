import { Activity, AlertTriangle, Bug, Timer } from "lucide-react";
import type { Severity } from "@/lib/scan-api";
import { SeverityBadgeClass } from "./severity";

const STATS = [
  { label: "Total Scans", value: "24", icon: Activity },
  { label: "Vulnerabilities Detected", value: "37", icon: Bug },
  { label: "High-Risk Issues", value: "8", icon: AlertTriangle },
  { label: "Average Scan Time", value: "1.8s", icon: Timer },
];

const RECENT_SCANS: {
  file: string;
  date: string;
  issues: number;
  severity: Severity;
  status: string;
}[] = [
  { file: "authentication.py", date: "Today, 10:42 AM", issues: 3, severity: "HIGH", status: "Completed" },
  { file: "database.py", date: "Yesterday", issues: 1, severity: "MEDIUM", status: "Completed" },
  { file: "utils.py", date: "Sep 2, 2026", issues: 0, severity: "LOW", status: "Completed" },
];

export function Dashboard() {
  return (
    <section id="dashboard" className="scroll-mt-20">
      <div className="mb-3">
        <h2 className="text-lg font-semibold tracking-tight text-foreground">Project Overview</h2>
        <p className="mt-1 text-sm text-muted-foreground">
          Aggregated activity across all scans in this workspace.
        </p>
      </div>

      <div className="grid gap-3 sm:grid-cols-2 xl:grid-cols-4">
        {STATS.map(({ label, value, icon: Icon }) => (
          <div key={label} className="rounded-md border border-border bg-card px-4 py-3.5">
            <div className="flex items-center justify-between">
              <span className="text-xs uppercase tracking-[0.06em] text-muted-foreground">
                {label}
              </span>
              <Icon className="h-4 w-4 text-muted-foreground" aria-hidden="true" />
            </div>
            <div className="mt-2 font-mono text-2xl font-semibold text-foreground">{value}</div>
          </div>
        ))}
      </div>

      <div className="mt-4 overflow-hidden rounded-md border border-border bg-card">
        <div className="border-b border-border bg-secondary/60 px-4 py-2.5">
          <h3 className="text-sm font-semibold tracking-tight text-foreground">Recent Scans</h3>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full min-w-[640px] text-left text-sm">
            <thead>
              <tr className="border-b border-border text-[11px] uppercase tracking-[0.06em] text-muted-foreground">
                <th className="px-4 py-2.5 font-medium">File Name</th>
                <th className="px-4 py-2.5 font-medium">Scan Date</th>
                <th className="px-4 py-2.5 font-medium">Issues Found</th>
                <th className="px-4 py-2.5 font-medium">Highest Severity</th>
                <th className="px-4 py-2.5 font-medium">Status</th>
              </tr>
            </thead>
            <tbody>
              {RECENT_SCANS.map((scan) => (
                <tr key={scan.file} className="border-b border-border last:border-b-0">
                  <td className="px-4 py-3 font-mono text-[13px] text-foreground">{scan.file}</td>
                  <td className="px-4 py-3 text-muted-foreground">{scan.date}</td>
                  <td className="px-4 py-3 font-mono text-foreground">{scan.issues}</td>
                  <td className="px-4 py-3">
                    <span className={SeverityBadgeClass(scan.severity)}>{scan.severity}</span>
                  </td>
                  <td className="px-4 py-3 text-muted-foreground">{scan.status}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </section>
  );
}
