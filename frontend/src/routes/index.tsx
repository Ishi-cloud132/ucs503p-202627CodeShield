import { createFileRoute } from "@tanstack/react-router";
import { useEffect, useRef, useState } from "react";
import { TopNav } from "@/components/codeshield/TopNav";
import { CodeEditor } from "@/components/codeshield/CodeEditor";
import { ScanSummary, SCAN_STEPS } from "@/components/codeshield/ScanSummary";
import { VulnerabilityResults } from "@/components/codeshield/VulnerabilityResults";
import {
  Dashboard,
  type ScanRecord,
} from "@/components/codeshield/Dashboard";
import { scanCode, type ScanResponse } from "@/lib/scan-api";
import { VULNERABLE_SAMPLE } from "@/lib/sample-code";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "CodeShield — Python Code Vulnerability Scanner" },
      {
        name: "description",
        content:
          "CodeShield analyzes Python source code with static analysis and machine learning to detect security vulnerabilities and produce a risk assessment report.",
      },
      { property: "og:title", content: "CodeShield — Python Code Vulnerability Scanner" },
      {
        property: "og:description",
        content:
          "Scan Python source code for SQL injection, command injection and hardcoded credentials, with severity, confidence and remediation guidance.",
      },
      { property: "og:type", content: "website" },
      { name: "twitter:card", content: "summary_large_image" },
    ],
  }),
  component: Index,
});

function Index() {
  const [code, setCode] = useState(VULNERABLE_SAMPLE);
  const [result, setResult] = useState<ScanResponse | null>(null);
  const [isScanning, setIsScanning] = useState(false);
  const [activeStep, setActiveStep] = useState(0);
  const [elapsed, setElapsed] = useState<string | null>(null);
  const timers = useRef<ReturnType<typeof setTimeout>[]>([]);
  const [scanHistory, setScanHistory] = useState<ScanRecord[]>([]);

 useEffect(() => {
  const savedScans = localStorage.getItem("codeshield_scan_history");

  if (savedScans) {
    try {
      setScanHistory(JSON.parse(savedScans));
    } catch {
      localStorage.removeItem("codeshield_scan_history");
    }
  }

  return () => timers.current.forEach(clearTimeout);
}, []);

  const handleScan = async () => {
    if (isScanning) return;
    timers.current.forEach(clearTimeout);
    timers.current = [];
    setIsScanning(true);
    setResult(null);
    setActiveStep(0);

    const started = performance.now();
    SCAN_STEPS.forEach((_, index) => {
      timers.current.push(setTimeout(() => setActiveStep(index), index * 380));
    });

    const [response] = await Promise.all([
      scanCode(code),
      new Promise((resolve) => timers.current.push(setTimeout(resolve, 1600))),
    ]);

    const scanDuration = Number(
  ((performance.now() - started) / 1000).toFixed(1)
);

setElapsed(`${scanDuration}s`);
setResult(response);

const vulnerabilities = response.vulnerabilities;

let highestSeverity: "HIGH" | "MEDIUM" | "LOW" = "LOW";

if (vulnerabilities.some((v) => v.severity === "HIGH")) {
  highestSeverity = "HIGH";
} else if (vulnerabilities.some((v) => v.severity === "MEDIUM")) {
  highestSeverity = "MEDIUM";
}

const newScan: ScanRecord = {
  id: `Python Code Scan #${scanHistory.length + 1}`,
  date: new Date().toLocaleString(),
  issues: response.total_vulnerabilities,
  severity: highestSeverity,
  duration: scanDuration,
};

const updatedHistory = [newScan, ...scanHistory];

setScanHistory(updatedHistory);

localStorage.setItem(
  "codeshield_scan_history",
  JSON.stringify(updatedHistory)
);

setIsScanning(false);
  };

  const flaggedLines = result ? result.vulnerabilities.map((v) => v.line) : [];

  return (
    <div className="min-h-screen bg-background">
      <TopNav />

      <main className="mx-auto max-w-[1400px] space-y-10 px-4 py-8 sm:px-6">
        <section id="scanner" className="scroll-mt-20">
          <h1 className="text-2xl font-semibold tracking-tight text-foreground">
            Code Security Scanner
          </h1>
          <p className="mt-1.5 max-w-3xl text-sm leading-relaxed text-muted-foreground">
            Analyze Python source code for potential security vulnerabilities using static analysis
            and machine learning.
          </p>

          <div className="mt-5 grid gap-4 lg:grid-cols-[minmax(0,1fr)_340px]">
            <CodeEditor
              code={code}
              onChange={setCode}
              onScan={handleScan}
              onLoadExample={() => {
                setCode(VULNERABLE_SAMPLE);
                setResult(null);
              }}
              isScanning={isScanning}
              flaggedLines={flaggedLines}
            />
            <ScanSummary
              result={result}
              isScanning={isScanning}
              activeStep={activeStep}
              elapsed={elapsed}
            />
          </div>
        </section>

        <VulnerabilityResults
          vulnerabilities={result?.vulnerabilities ?? []}
          hasScanned={Boolean(result)}
        />

        <Dashboard scans={scanHistory} />
      </main>

      <footer className="border-t border-border">
        <div className="mx-auto flex max-w-[1400px] flex-col gap-1 px-4 py-6 text-xs text-muted-foreground sm:flex-row sm:items-center sm:justify-between sm:px-6">
          <span>CodeShield · ML-Based Code Vulnerability Detection and Risk Assessment</span>
          <span className="font-mono">Engine v2.4 · Ruleset 128 · Python 3</span>
        </div>
      </footer>
    </div>
  );
}
