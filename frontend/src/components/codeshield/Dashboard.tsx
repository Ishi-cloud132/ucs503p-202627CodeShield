import { Activity, AlertTriangle, Bug, Timer } from "lucide-react";
import type { Severity } from "@/lib/scan-api";
import { SeverityBadgeClass } from "./severity";

export type ScanRecord = {
  id: string;
  date: string;
  issues: number;
  severity: Severity;
  duration: number;
};

type DashboardProps = {
  scans: ScanRecord[];
};

export function Dashboard({ scans }: DashboardProps) {
  const totalScans = scans.length;

  const totalVulnerabilities = scans.reduce(
    (total, scan) => total + scan.issues,
    0
  );

  const highRiskIssues = scans.reduce(
    (total, scan) =>
      total + (scan.severity === "HIGH" ? scan.issues : 0),
    0
  );

  const averageScanTime =
    totalScans > 0
      ? (
          scans.reduce((total, scan) => total + scan.duration, 0) /
          totalScans
        ).toFixed(1)
      : "0.0";

  const stats = [
    {
      label: "Total Scans",
      value: String(totalScans),
      icon: Activity,
    },
    {
      label: "Vulnerabilities Detected",
      value: String(totalVulnerabilities),
      icon: Bug,
    },
    {
      label: "High-Risk Issues",
      value: String(highRiskIssues),
      icon: AlertTriangle,
    },
    {
      label: "Average Scan Time",
      value: `${averageScanTime}s`,
      icon: Timer,
    },
  ];

  return (
    <section id="dashboard" className="scroll-mt-20">
      <div className="mb-3">
        <h2 className="text-lg font-semibold tracking-tight text-foreground">
          Project Overview
        </h2>
        <p className="mt-1 text-sm text-muted-foreground">
          Aggregated activity across all scans in this workspace.
        </p>
      </div>

      <div className="grid gap-3 sm:grid-cols-2 xl:grid-cols-4">
        {stats.map(({ label, value, icon: Icon }) => (
          <div
            key={label}
            className="rounded-md border border-border bg-card px-4 py-3.5"
          >
            <div className="flex items-center justify-between">
              <span className="text-xs uppercase tracking-[0.06em] text-muted-foreground">
                {label}
              </span>

              <Icon
                className="h-4 w-4 text-muted-foreground"
                aria-hidden="true"
              />
            </div>

            <div className="mt-2 font-mono text-2xl font-semibold text-foreground">
              {value}
            </div>
          </div>
        ))}
      </div>

      <div className="mt-4 overflow-hidden rounded-md border border-border bg-card">
        <div className="border-b border-border bg-secondary/60 px-4 py-2.5">
          <h3 className="text-sm font-semibold tracking-tight text-foreground">
            Recent Scans
          </h3>
        </div>

        {scans.length === 0 ? (
          <div className="px-4 py-8 text-center text-sm text-muted-foreground">
            No scans performed yet.
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full min-w-[640px] text-left text-sm">
              <thead>
                <tr className="border-b border-border text-[11px] uppercase tracking-[0.06em] text-muted-foreground">
                  <th className="px-4 py-2.5 font-medium">Scan</th>
                  <th className="px-4 py-2.5 font-medium">Scan Date</th>
                  <th className="px-4 py-2.5 font-medium">Issues Found</th>
                  <th className="px-4 py-2.5 font-medium">
                    Highest Severity
                  </th>
                  <th className="px-4 py-2.5 font-medium">Status</th>
                </tr>
              </thead>

              <tbody>
                {scans.slice(0, 5).map((scan) => (
                  <tr
                    key={scan.id}
                    className="border-b border-border last:border-b-0"
                  >
                    <td className="px-4 py-3 font-mono text-[13px] text-foreground">
                      {scan.id}
                    </td>

                    <td className="px-4 py-3 text-muted-foreground">
                      {scan.date}
                    </td>

                    <td className="px-4 py-3 font-mono text-foreground">
                      {scan.issues}
                    </td>

                    <td className="px-4 py-3">
                      <span className={SeverityBadgeClass(scan.severity)}>
                        {scan.severity}
                      </span>
                    </td>

                    <td className="px-4 py-3 text-muted-foreground">
                      Completed
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </section>
  );
}