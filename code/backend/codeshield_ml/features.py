"""AST-derived structural features for CodeShield.

The transformer is intentionally defensive: malformed or non-Python snippets
receive zero AST features, while lexical indicators are still extracted.
"""
from __future__ import annotations

import ast
import re
from collections import Counter

import numpy as np
from scipy.sparse import csr_matrix
from sklearn.base import BaseEstimator, TransformerMixin


FEATURE_NAMES = [
    "ast_parse_success", "imports", "import_from", "function_defs",
    "class_defs", "assignments", "calls", "attributes", "string_constants",
    "subprocess_calls", "os_system_calls", "eval_exec_calls", "open_calls",
    "file_path_calls", "pickle_calls", "input_calls", "sql_keywords",
    "html_markers", "shell_markers", "path_traversal_markers",
    "try_blocks", "with_blocks", "loops", "comprehensions",
    "return_nodes", "exception_handlers", "fstring_nodes",
]

SQL_RE = re.compile(r"\b(select|insert|update|delete|drop|union|where|execute)\b", re.I)
HTML_RE = re.compile(r"<\s*(script|iframe|img|svg)|javascript\s*:", re.I)
SHELL_RE = re.compile(r"\b(os\.system|subprocess\.(run|call|Popen)|shell\s*=\s*True)\b", re.I)
PATH_RE = re.compile(r"\.\./|%2e%2e|\\\\\.\.\\\\", re.I)


class ASTStructuralFeatures(BaseEstimator, TransformerMixin):
    """Convert source-code strings into a compact numeric feature matrix."""

    def fit(self, X, y=None):
        return self

    @staticmethod
    def _call_name(node):
        parts = []
        while isinstance(node, ast.Attribute):
            parts.append(node.attr)
            node = node.value
        if isinstance(node, ast.Name):
            parts.append(node.id)
        return ".".join(reversed(parts))

    def _one(self, code):
        code = "" if code is None else str(code)
        values = Counter()
        values["sql_keywords"] = len(SQL_RE.findall(code))
        values["html_markers"] = len(HTML_RE.findall(code))
        values["shell_markers"] = len(SHELL_RE.findall(code))
        values["path_traversal_markers"] = len(PATH_RE.findall(code))

        try:
            tree = ast.parse(code)
            values["ast_parse_success"] = 1
        except (SyntaxError, ValueError, TypeError):
            return [float(values[name]) for name in FEATURE_NAMES]

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                values["imports"] += 1
            elif isinstance(node, ast.ImportFrom):
                values["import_from"] += 1
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                values["function_defs"] += 1
            elif isinstance(node, ast.ClassDef):
                values["class_defs"] += 1
            elif isinstance(node, (ast.Assign, ast.AnnAssign, ast.AugAssign)):
                values["assignments"] += 1
            elif isinstance(node, ast.Call):
                values["calls"] += 1
                name = self._call_name(node.func).lower()
                if name in {"os.system", "system"}:
                    values["os_system_calls"] += 1
                if name.startswith("subprocess.") or name == "popen":
                    values["subprocess_calls"] += 1
                if name in {"eval", "exec", "builtins.eval", "builtins.exec"}:
                    values["eval_exec_calls"] += 1
                if name in {"open", "io.open"} or name.endswith(".open"):
                    values["open_calls"] += 1
                if any(token in name for token in ("path.join", "path.abspath",
                                                    "path.normpath", "pathlib")):
                    values["file_path_calls"] += 1
                if "pickle." in name or name.startswith("pickle"):
                    values["pickle_calls"] += 1
                if name == "input":
                    values["input_calls"] += 1
            elif isinstance(node, ast.Attribute):
                values["attributes"] += 1
            elif isinstance(node, ast.Constant) and isinstance(node.value, str):
                values["string_constants"] += 1
            elif isinstance(node, ast.Try):
                values["try_blocks"] += 1
                values["exception_handlers"] += len(node.handlers)
            elif isinstance(node, (ast.With, ast.AsyncWith)):
                values["with_blocks"] += 1
            elif isinstance(node, (ast.For, ast.AsyncFor, ast.While)):
                values["loops"] += 1
            elif isinstance(node, (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)):
                values["comprehensions"] += 1
            elif isinstance(node, ast.Return):
                values["return_nodes"] += 1
            elif isinstance(node, ast.JoinedStr):
                values["fstring_nodes"] += 1

        return [float(values[name]) for name in FEATURE_NAMES]

    def transform(self, X):
        rows = [self._one(code) for code in X]
        return csr_matrix(np.asarray(rows, dtype=np.float32))
