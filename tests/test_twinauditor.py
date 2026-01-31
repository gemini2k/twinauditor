import unittest

from twinauditor import analyze_text, AuditResult


class AnalyzeTextTests(unittest.TestCase):
    def test_analyze_text_counts_lines(self) -> None:
        text = """
        INFO booting
        warn disk nearly full
        error failed to load
        warning retrying
        """
        result = analyze_text(text)
        self.assertEqual(
            result,
            AuditResult(total_lines=4, error_lines=1, warning_lines=2),
        )

    def test_error_rate_handles_empty_text(self) -> None:
        result = analyze_text("\n\n")
        self.assertEqual(result.total_lines, 0)
        self.assertEqual(result.error_rate, 0.0)


if __name__ == "__main__":
    unittest.main()
