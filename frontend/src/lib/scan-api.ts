export type Severity = "CRITICAL" | "HIGH" | "MEDIUM" | "LOW";

export type DetectionMethod = "static" | "ml";

export interface Vulnerability {
  type: string;
  severity: Severity;
  line: number | null;
  confidence: number;
  risk_score: number;
  description: string;
  recommendation: string;
  cwe?: string | null;
  detection_method?: "static" | "ml";
}

export interface MLAssessment {
  label: string;
  vulnerability_type: string | null;
  is_vulnerable: boolean;
  confidence: number;
  severity: Severity | "NONE";
  cwe: string | null;
  risk_score: number;
}

export interface ScanResponse {
  success?: boolean;
  total_vulnerabilities: number;
  vulnerabilities: Vulnerability[];
  overall_risk?: Severity | "NONE";
  ml_assessment?: {
    label: string;
    vulnerability_type: string | null;
    is_vulnerable: boolean;
    confidence: number;
    severity: Severity | "NONE";
    cwe: string | null;
    risk_score: number;
  } | null;
  source?: "backend" | "mock" | "static+ml";
}


// ============================================================
// API ENDPOINT
// ============================================================

export const SCAN_ENDPOINT = "http://127.0.0.1:8000/scan";


// ============================================================
// MOCK DATA
// ============================================================

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

    cwe: "CWE-89",
    detection_method: "static",
  },

  {
    type: "Command Injection",
    severity: "CRITICAL",
    line: 6,
    confidence: 0.91,
    risk_score: 10,

    description:
      "A shell command is constructed from untrusted input and passed to os.system(), which executes it through the system shell.",

    recommendation:
      "Use subprocess.run() with an argument list and shell=False, and validate any user-supplied values.",

    cwe: "CWE-78",
    detection_method: "static",
  },

  {
    type: "Hardcoded Credentials",
    severity: "HIGH",
    line: 3,
    confidence: 0.86,
    risk_score: 9,

    description:
      "A credential is stored as a literal string in source code. Anyone with repository access can read it.",

    recommendation:
      "Load secrets from environment variables or a managed secret store, and rotate the exposed credential.",

    cwe: "CWE-798",
    detection_method: "static",
  },
];


// ============================================================
// MOCK SCAN
// ============================================================

export function mockScan(): ScanResponse {
  return {
    success: true,

    total_vulnerabilities:
      MOCK_VULNERABILITIES.length,

    vulnerabilities:
      MOCK_VULNERABILITIES,

    overall_risk: "CRITICAL",

    source: "mock",
  };
}


// ============================================================
// REAL BACKEND SCAN
// ============================================================

/**
 * Calls the FastAPI detection service.
 *
 * The backend performs:
 *
 *     Static Analysis + Machine Learning
 *
 * and returns a unified vulnerability report.
 *
 * Mock results are used only if the backend is unreachable.
 */
export async function scanCode(
  code: string
): Promise<ScanResponse> {

  try {

    const controller = new AbortController();

    const timeout = setTimeout(
      () => controller.abort(),
      15000
    );

    const res = await fetch(
      SCAN_ENDPOINT,
      {
        method: "POST",

        headers: {
          "Content-Type": "application/json",
        },

        body: JSON.stringify({
          code,
        }),

        signal: controller.signal,
      }
    );

    clearTimeout(timeout);

    if (!res.ok) {
      throw new Error(
        `Scan failed with status ${res.status}`
      );
    }

    const data =
      (await res.json()) as ScanResponse;

    return {
      ...data,
      source: "backend",
    };

  } catch (error) {

    console.error(
      "CodeShield backend scan failed:",
      error
    );

    return mockScan();
  }
}