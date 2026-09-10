export type Severity = "HIGH" | "MEDIUM" | "LOW";

export interface Vulnerability {
  type: string;
  severity: Severity;
  line: number;
  confidence: number;
  risk_score: number;
  description: string;
  recommendation: string;
}

export interface ScanResponse {
  total_vulnerabilities: number;
  vulnerabilities: Vulnerability[];
  source?: "backend" | "mock";
}

export const SCAN_ENDPOINT = "http://127.0.0.1:8000/scan";

const MOCK_VULNERABILITIES: Vulnerability[] = [
  {
    type: "SQL Injection",
    severity: "HIGH",
    line: 5,
    confidence: 0.94,
    risk_score: 9,
    description:
      "User-controlled input appears to be directly concatenated into an SQL query, allowing an attacker to alter the statement executed by the database.",
    recommendation:
      "Use parameterized queries instead of directly inserting user input into SQL statements.",
  },
  {
    type: "Command Injection",
    severity: "HIGH",
    line: 6,
    confidence: 0.91,
    risk_score: 9,
    description:
      "A shell command is constructed from untrusted input and passed to os.system(), which executes it through the system shell.",
    recommendation:
      "Use subprocess.run() with an argument list and shell=False, and validate any user-supplied values.",
  },
  {
    type: "Hardcoded Credentials",
    severity: "MEDIUM",
    line: 3,
    confidence: 0.86,
    risk_score: 6,
    description:
      "A credential is stored as a literal string in source code. Anyone with repository access can read it.",
    recommendation:
      "Load secrets from environment variables or a managed secret store, and rotate the exposed credential.",
  },
];

export function mockScan(): ScanResponse {
  return {
    total_vulnerabilities: MOCK_VULNERABILITIES.length,
    vulnerabilities: MOCK_VULNERABILITIES,
    source: "mock",
  };
}

/**
 * Calls the FastAPI detection service. Falls back to mock analysis results
 * when the backend is not reachable so the UI can be demonstrated standalone.
 */
export async function scanCode(code: string): Promise<ScanResponse> {
  try {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 4000);
    const res = await fetch(SCAN_ENDPOINT, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ code }),
      signal: controller.signal,
    });
    clearTimeout(timeout);
    if (!res.ok) throw new Error(`Scan failed with status ${res.status}`);
    const data = (await res.json()) as ScanResponse;
    return { ...data, source: "backend" };
  } catch {
    return mockScan();
  }
}
