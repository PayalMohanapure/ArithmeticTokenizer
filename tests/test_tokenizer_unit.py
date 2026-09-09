"""Unit Tests for Arithmetic Expression Tokenizer Core."""

import sys
from pathlib import Path

# Ensure project root in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import pytest

from ui.lexer_runner import run_lexer, find_lexer_executable
from ui.token_parser import parse_lexer_output
from ui.statistics import calculate_statistics, format_save_report


def test_lexer_binary_found():
    exe = find_lexer_executable()
    assert exe is not None
    assert exe.name == "lexer.exe"
    assert exe.is_file()


@pytest.mark.parametrize(
    "expression, expected_types, expected_stats",
    [
        (
            "10 + 20",
            ["INTEGER", "PLUS", "INTEGER"],
            {"total": 3, "identifiers": 0, "numbers": 2, "operators": 1, "parentheses": 0, "errors": 0},
        ),
        (
            "x = 10 + 20 * 5",
            ["IDENTIFIER", "ASSIGN", "INTEGER", "PLUS", "INTEGER", "MULTIPLY", "INTEGER"],
            {"total": 7, "identifiers": 1, "numbers": 3, "operators": 3, "parentheses": 0, "errors": 0},
        ),
        (
            "result = 12.5 + 3.14 * (x - 2)",
            ["IDENTIFIER", "ASSIGN", "FLOAT", "PLUS", "FLOAT", "MULTIPLY", "LPAREN", "IDENTIFIER", "MINUS", "INTEGER", "RPAREN"],
            {"total": 11, "identifiers": 2, "numbers": 3, "operators": 4, "parentheses": 2, "errors": 0},
        ),
        (
            "a = b ^ 2 % 5",
            ["IDENTIFIER", "ASSIGN", "IDENTIFIER", "POWER", "INTEGER", "MODULO", "INTEGER"],
            {"total": 7, "identifiers": 2, "numbers": 2, "operators": 3, "parentheses": 0, "errors": 0},
        ),
        (
            "total = price * quantity + tax",
            ["IDENTIFIER", "ASSIGN", "IDENTIFIER", "MULTIPLY", "IDENTIFIER", "PLUS", "IDENTIFIER"],
            {"total": 7, "identifiers": 4, "numbers": 0, "operators": 3, "parentheses": 0, "errors": 0},
        ),
    ],
)
def test_valid_expressions(expression, expected_types, expected_stats):
    res = run_lexer(expression)
    assert res.success, f"Lexer failed on expression: {expression} -> {res.error_message}"
    parsed = parse_lexer_output(res.raw_output)
    stats = calculate_statistics(parsed.tokens, parsed.errors)

    actual_types = [t.token_type for t in parsed.tokens]
    assert actual_types == expected_types

    assert stats.total_tokens == expected_stats["total"]
    assert stats.identifiers == expected_stats["identifiers"]
    assert stats.numbers == expected_stats["numbers"]
    assert stats.operators == expected_stats["operators"]
    assert stats.parentheses == expected_stats["parentheses"]
    assert stats.errors == expected_stats["errors"]


def test_lexical_error_detection():
    expr = "x = 10 @ 20"
    res = run_lexer(expr)
    assert res.success
    parsed = parse_lexer_output(res.raw_output)
    stats = calculate_statistics(parsed.tokens, parsed.errors)

    assert len(parsed.errors) == 1
    assert parsed.errors[0].lexeme == "@"
    assert parsed.errors[0].token_type == "ERROR"
    assert parsed.errors[0].is_error is True
    assert stats.errors == 1
    assert stats.total_tokens == 4


def test_missing_lexer_graceful():
    res = run_lexer("10 + 20", lexer_path="nonexistent_binary.exe")
    assert not res.success
    assert "FLEX tokenizer executable not found" in res.error_message


def test_save_report_content():
    expr = "x = 25 + 3.14 * (y - 10)"
    res = run_lexer(expr)
    assert res.success
    parsed = parse_lexer_output(res.raw_output)
    stats = calculate_statistics(parsed.tokens, parsed.errors)
    report = format_save_report(expr, parsed.tokens, stats, parsed.errors)

    assert "ARITHMETIC EXPRESSION TOKENIZER" in report
    assert "x = 25 + 3.14 * (y - 10)" in report
    assert "IDENTIFIER" in report
    assert "Total Tokens: 11" in report
    assert "No lexical errors detected." in report
