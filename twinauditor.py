"""Simple auditing utilities for log text."""

from __future__ import annotations

import argparse
from dataclasses import dataclass


@dataclass(frozen=True)
class AuditResult:
    total_lines: int
    error_lines: int
    warning_lines: int

    @property
    def error_rate(self) -> float:
        if self.total_lines == 0:
            return 0.0
        return self.error_lines / self.total_lines


ERROR_PREFIXES = ("error", "err")
WARNING_PREFIXES = ("warn", "warning")


def analyze_text(text: str) -> AuditResult:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    error_lines = sum(_has_prefix(line, ERROR_PREFIXES) for line in lines)
    warning_lines = sum(_has_prefix(line, WARNING_PREFIXES) for line in lines)
    return AuditResult(total_lines=len(lines), error_lines=error_lines, warning_lines=warning_lines)


def _has_prefix(line: str, prefixes: tuple[str, ...]) -> bool:
    lowered = line.lower()
    return any(lowered.startswith(prefix) for prefix in prefixes)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Summarize log text for errors and warnings.")
    parser.add_argument("path", help="Path to a text file to analyze.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    with open(args.path, "r", encoding="utf-8") as handle:
        result = analyze_text(handle.read())
    print(f"Total lines: {result.total_lines}")
    print(f"Error lines: {result.error_lines}")
    print(f"Warning lines: {result.warning_lines}")
    print(f"Error rate: {result.error_rate:.2%}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
