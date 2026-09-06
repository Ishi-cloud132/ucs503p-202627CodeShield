import { Check, CircleDot, Loader2, ShieldAlert } from "lucide-react";
import type { ScanResponse, Severity } from "@/lib/scan-api";
import { severityStyles } from "./severity";

export const SCAN_STEPS = [
  "Parsing source code",
  "Performing static analysis",
  "Running vulnerability classifier",
  "Calculating risk assessment",
];

interface ScanSummaryProps {
  result: ScanResponse | null;
  isScanning: boolean;
  activeStep: number;
  elapsed: string | null;
}

function overallSeverity(result: ScanResponse): Severity {
  if (result.vulnerabilities.some((v) => v.severity === "HIGH")) return "HIGH";
  if (result.vulnerabilities.some((v) => v.severity === "MEDIUM")) return "MEDIUM";
  return "LOW";
}

function StatRow({
  label,
  value,
  accent,
}: {
  label: string;
  value: string | number;
  accent?: string;
}) {
  return (
    <div className="flex items-center justify-between border-b border-border py-2.5 last:border-b-0">
      <span className="text-sm text-muted-foreground">{label}</span>
      <span className={`font-mono text-sm font-semibold ${accent ?? "text-foreground"}`}>
        {value}
      </span>
    </div>
  );
}

export function ScanSummary({ result, isScanning, activeStep, elapsed }: ScanSummaryProps) {
  return (
    <section className="flex flex-col rounded-md border border-border bg-card">
      <div className="border-b border-border bg-secondary/60 px-4 py-2.5">
        <h3 className="text-sm font-semibold tracking-tight text-foreground">Scan Summary</h3>
      </div>

      <div className="px-4 py-3">
        {isScanning ? (
          <div>
            <div className="flex items-center gap-2 text-sm text-foreground">
              <Loader2 className="h-4 w-4 animate-spin text-primary" aria-hidden="true" />
              Analyzing source code...
            </div>
            <ol className="mt-4 space-y-2.5">
              {SCAN_STEPS.map((step, index) => {
                const done = index < activeStep;
                const current = index === activeStep;
                return (
                  <li
                    key={step}
                    className={`flex items-center gap-2 text-sm ${
                      done ? "text-foreground" : current ? "text-foreground" : "text-muted-foreground/60"
                    }`}
                  >
                    {done ? (
                      <Check className="h-4 w-4 text-severity-low" aria-hidden="true" />
                    ) : current ? (
                      <Loader2 className="h-4 w-4 animate-spin text-primary" aria-hidden="true" />
                    ) : (
                      <CircleDot className="h-4 w-4 opacity-40" aria-hidden="true" />
                    )}
                    {step}
                  </li>
                );
              })}
            </ol>
          </div>
        ) : result ? (
          <div>
            <div
              className={`mb-3 flex items-center justify-between rounded border px-3 py-2.5 ${severityStyles[overallSeverity(result)].badge}`}
            >
              <span className="flex items-center gap-2 text-xs font-semibold uppercase tracking-[0.08em]">
                <ShieldAlert className="h-4 w-4" aria-hidden="true" />
                Security Risk
              </span>
              <span className="font-mono text-sm font-bold">{overallSeverity(result)}</span>
            </div>

            <StatRow label="Total Issues" value={result.total_vulnerabilities} />
            <StatRow
              label="High Risk"
              value={result.vulnerabilities.filter((v) => v.severity === "HIGH").length}
              accent="text-severity-high"
            />
            <StatRow
              label="Medium Risk"
              value={result.vulnerabilities.filter((v) => v.severity === "MEDIUM").length}
              accent="text-severity-medium"
            />
            <StatRow
              label="Low Risk"
              value={result.vulnerabilities.filter((v) => v.severity === "LOW").length}
              accent="text-severity-low"
            />
            <StatRow label="Scan Duration" value={elapsed ?? "—"} />
            <StatRow
              label="Analysis Source"
              value={result.source === "backend" ? "FastAPI service" : "Local model (offline)"}
            />
          </div>
        ) : (
          <div>
            <div className="mb-3 flex items-center justify-between rounded border border-border bg-secondary/50 px-3 py-2.5">
              <span className="text-xs font-semibold uppercase tracking-[0.08em] text-muted-foreground">
                Status
              </span>
              <span className="font-mono text-sm text-foreground">Ready to scan</span>
            </div>
            <StatRow label="Supported Language" value="Python 3" />
            <StatRow label="Detection Engine" value="Active" accent="text-severity-low" />
            <StatRow label="Ruleset" value="v2.4 · 128 rules" />
            <StatRow label="Classifier" value="RandomForest · CWE" />
            <p className="pt-3 text-xs leading-relaxed text-muted-foreground">
              Paste Python source into the editor and run a scan. Static analysis findings are
              scored by the ML classifier to produce a risk assessment.
            </p>
          </div>
        )}
      </div>
    </section>
  );
}
