"""Adapter exposing the existing static analyzer through the ML package."""

try:
    from ..analyzers.static_analyzer import analyze_code
except ImportError:
    from analyzers.static_analyzer import analyze_code


def run_static_rules(code: str) -> list[dict]:
    return analyze_code(code)