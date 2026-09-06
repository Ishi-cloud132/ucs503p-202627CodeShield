import { useMemo, useRef, type ChangeEvent, type UIEvent } from "react";
import { FileCode2, Play, Loader2, FileWarning } from "lucide-react";

const KEYWORDS = new Set([
  "import","from","def","return","if","elif","else","for","while","in","not","and","or",
  "class","try","except","finally","with","as","pass","break","continue","lambda","yield",
  "None","True","False","global","raise","assert","del","is","async","await",
]);
const BUILTINS = new Set([
  "print","input","open","len","range","str","int","float","list","dict","set","os","sys",
  "eval","exec","subprocess","sqlite3","format","join","connect","execute","system","fetchall",
]);

function escapeHtml(value: string) {
  return value
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

function highlightPython(source: string) {
  return source
    .split("\n")
    .map((line) => {
      const commentIndex = findCommentIndex(line);
      const codePart = commentIndex === -1 ? line : line.slice(0, commentIndex);
      const comment = commentIndex === -1 ? "" : line.slice(commentIndex);

      const html = escapeHtml(codePart).replace(
        /("[^"]*"|'[^']*')|\b(\d+(?:\.\d+)?)\b|\b([A-Za-z_][A-Za-z0-9_]*)\b/g,
        (match, str, num, word) => {
          if (str) return `<span class="tok-str">${match}</span>`;
          if (num) return `<span class="tok-num">${match}</span>`;
          if (word && KEYWORDS.has(word)) return `<span class="tok-kw">${match}</span>`;
          if (word && BUILTINS.has(word)) return `<span class="tok-bi">${match}</span>`;
          return match;
        },
      );

      const commentHtml = comment ? `<span class="tok-com">${escapeHtml(comment)}</span>` : "";
      return `${html}${commentHtml}` || "&nbsp;";
    })
    .join("\n");
}

function findCommentIndex(line: string) {
  let inSingle = false;
  let inDouble = false;
  for (let i = 0; i < line.length; i += 1) {
    const ch = line[i];
    if (ch === "'" && !inDouble) inSingle = !inSingle;
    else if (ch === '"' && !inSingle) inDouble = !inDouble;
    else if (ch === "#" && !inSingle && !inDouble) return i;
  }
  return -1;
}

interface CodeEditorProps {
  code: string;
  onChange: (value: string) => void;
  onScan: () => void;
  onLoadExample: () => void;
  isScanning: boolean;
  flaggedLines: number[];
}

export function CodeEditor({
  code,
  onChange,
  onScan,
  onLoadExample,
  isScanning,
  flaggedLines,
}: CodeEditorProps) {
  const preRef = useRef<HTMLPreElement>(null);
  const gutterRef = useRef<HTMLDivElement>(null);

  const lines = useMemo(() => code.split("\n"), [code]);
  const highlighted = useMemo(() => highlightPython(code), [code]);

  const handleScroll = (event: UIEvent<HTMLTextAreaElement>) => {
    const target = event.currentTarget;
    if (preRef.current) {
      preRef.current.scrollTop = target.scrollTop;
      preRef.current.scrollLeft = target.scrollLeft;
    }
    if (gutterRef.current) gutterRef.current.scrollTop = target.scrollTop;
  };

  return (
    <section className="flex flex-col overflow-hidden rounded-md border border-border bg-card">
      <div className="flex items-center justify-between gap-3 border-b border-border bg-secondary/60 px-3 py-2">
        <div className="flex items-center gap-2 text-sm text-foreground">
          <FileCode2 className="h-4 w-4 text-muted-foreground" aria-hidden="true" />
          <span className="font-mono text-[13px]">main.py</span>
        </div>
        <div className="flex items-center gap-3 text-[11px] uppercase tracking-[0.08em] text-muted-foreground">
          <span>UTF-8</span>
          <span className="rounded border border-border px-1.5 py-0.5 text-foreground">Python</span>
        </div>
      </div>

      <div className="relative flex h-[420px] bg-editor font-mono text-[13px] leading-6">
        <div
          ref={gutterRef}
          className="select-none overflow-hidden border-r border-border bg-editor py-3 text-right"
          aria-hidden="true"
        >
          {lines.map((_, index) => {
            const lineNumber = index + 1;
            const flagged = flaggedLines.includes(lineNumber);
            return (
              <div
                key={lineNumber}
                className={`px-3 ${flagged ? "bg-severity-high-soft text-severity-high" : "text-muted-foreground/60"}`}
              >
                {lineNumber}
              </div>
            );
          })}
        </div>

        <div className="relative flex-1">
          <pre
            ref={preRef}
            aria-hidden="true"
            className="pointer-events-none absolute inset-0 overflow-auto whitespace-pre px-3 py-3 text-foreground"
            dangerouslySetInnerHTML={{ __html: highlighted }}
          />
          <textarea
            value={code}
            spellCheck={false}
            onScroll={handleScroll}
            onChange={(event: ChangeEvent<HTMLTextAreaElement>) => onChange(event.target.value)}
            aria-label="Python source code"
            className="absolute inset-0 resize-none overflow-auto whitespace-pre bg-transparent px-3 py-3 font-mono text-[13px] leading-6 text-transparent caret-foreground outline-none"
          />
        </div>
      </div>

      <div className="flex flex-col gap-2 border-t border-border bg-secondary/40 px-3 py-3 sm:flex-row sm:items-center sm:justify-between">
        <button
          type="button"
          onClick={onLoadExample}
          className="inline-flex items-center justify-center gap-2 rounded-md border border-border bg-card px-3 py-2 text-sm text-foreground transition-colors hover:bg-accent"
        >
          <FileWarning className="h-4 w-4 text-severity-medium" aria-hidden="true" />
          Load Vulnerable Example
        </button>
        <button
          type="button"
          onClick={onScan}
          disabled={isScanning}
          className="inline-flex items-center justify-center gap-2 rounded-md bg-primary px-4 py-2 text-sm font-semibold text-primary-foreground transition-colors hover:bg-primary/90 disabled:cursor-not-allowed disabled:opacity-60"
        >
          {isScanning ? (
            <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" />
          ) : (
            <Play className="h-4 w-4" aria-hidden="true" />
          )}
          {isScanning ? "Scanning..." : "Scan Code"}
        </button>
      </div>
    </section>
  );
}
