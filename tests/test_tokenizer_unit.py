"""Unit Tests for C-Language Compiler Tokenizer Core."""

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
    """Verify that lexer.exe exists and is accessible."""
    exe = find_lexer_executable()
    assert exe is not None
    assert exe.name == "lexer.exe"
    assert exe.is_file()


def test_keyword_recognition():
    """Test recognition of C keywords."""
    code = "int float char double void if else for while do switch case default break continue return struct sizeof"
    res = run_lexer(code)
    assert res.success
    parsed = parse_lexer_output(res.raw_output)
    stats = calculate_statistics(parsed.tokens, parsed.errors)

    assert stats.keywords == 18
    assert all(t.category == "Keyword" for t in parsed.tokens)
    assert stats.errors == 0


def test_arithmetic_and_assignment_operators():
    """Test arithmetic expressions and assignment operators."""
    code = "int a = 10 + 20 * 5 - (a / 2) % 3; a += 1; b *= 2;"
    res = run_lexer(code)
    assert res.success
    parsed = parse_lexer_output(res.raw_output)
    stats = calculate_statistics(parsed.tokens, parsed.errors)

    assert stats.keywords == 1  # 'int'
    assert stats.operators > 5
    assert stats.errors == 0


def test_if_else_and_relational_logical_operators():
    """Test if-else statements with relational and logical operators."""
    code = """
    if (x >= 10 && y < 20 || z != 0) {
        x = 1;
    } else {
        x = 0;
    }
    """
    res = run_lexer(code)
    assert res.success
    parsed = parse_lexer_output(res.raw_output)
    stats = calculate_statistics(parsed.tokens, parsed.errors)

    assert stats.keywords >= 2  # 'if', 'else'
    assert stats.errors == 0
    token_types = [t.token_type for t in parsed.tokens]
    assert "GE_OP" in token_types
    assert "LT_OP" in token_types
    assert "NE_OP" in token_types
    assert "LOGICAL_AND" in token_types
    assert "LOGICAL_OR" in token_types


def test_do_while_and_for_loops():
    """Test do-while and for loops."""
    code = """
    do {
        count++;
    } while (count < 10);

    for (int i = 0; i < 5; i++) {
        sum += i;
    }
    """
    res = run_lexer(code)
    assert res.success
    parsed = parse_lexer_output(res.raw_output)
    stats = calculate_statistics(parsed.tokens, parsed.errors)

    assert stats.keywords >= 4  # 'do', 'while', 'for', 'int'
    assert stats.errors == 0
    types = [t.token_type for t in parsed.tokens]
    assert "INC_OP" in types
    assert "ADD_ASSIGN" in types


def test_function_definition():
    """Test function definition and return statement."""
    code = """
    int add(int a, int b) {
        return a + b;
    }
    """
    res = run_lexer(code)
    assert res.success
    parsed = parse_lexer_output(res.raw_output)
    stats = calculate_statistics(parsed.tokens, parsed.errors)

    assert stats.keywords == 4  # 3 'int' + 1 'return'
    assert stats.identifiers >= 3  # 'add', 'a', 'b'
    assert stats.errors == 0


def test_strings_chars_and_comments():
    """Test string literals, character constants, and comments."""
    code = """
    // Single line comment
    /* Multi
       Line */
    char letter = 'A';
    char *str = "Hello Compiler!";
    """
    res = run_lexer(code)
    assert res.success
    parsed = parse_lexer_output(res.raw_output)
    stats = calculate_statistics(parsed.tokens, parsed.errors)

    assert stats.comments == 2
    types = [t.token_type for t in parsed.tokens]
    assert "CHAR_LITERAL" in types
    assert "STRING_LITERAL" in types
    assert stats.errors == 0


def test_preprocessor_directives():
    """Test preprocessor macros and headers."""
    code = """
    #include <stdio.h>
    #define MAX 100
    """
    res = run_lexer(code)
    assert res.success
    parsed = parse_lexer_output(res.raw_output)
    stats = calculate_statistics(parsed.tokens, parsed.errors)

    assert stats.preprocessors >= 2
    types = [t.token_type for t in parsed.tokens]
    assert "PREPROCESSOR" in types
    assert "HEADER_FILE" in types
    assert stats.errors == 0


def test_lexical_error_detection():
    """Test that invalid characters generate ERROR tokens and error diagnostics."""
    code = "int x = 10 @ 20; float val$ = 3.14; int `bad` = 5;"
    res = run_lexer(code)
    assert res.success
    parsed = parse_lexer_output(res.raw_output)
    stats = calculate_statistics(parsed.tokens, parsed.errors)

    assert stats.errors >= 3
    error_lexemes = [e.lexeme for e in parsed.errors]
    assert "@" in error_lexemes
    assert "$" in error_lexemes
    assert "`" in error_lexemes
    assert all(e.is_error for e in parsed.errors)


def test_symbol_table_generation():
    """Test consolidated Symbol Table generation."""
    code = """
    int main() {
        int x = 10;
        int y = x + 5;
        return x;
    }
    """
    res = run_lexer(code)
    assert res.success
    parsed = parse_lexer_output(res.raw_output)
    sym_table = parsed.get_symbol_table()

    assert len(sym_table) > 0
    # Check that 'x' has count 3
    x_entries = [e for e in sym_table if e.lexeme == "x"]
    assert len(x_entries) == 1
    assert x_entries[0].count == 3
    assert len(x_entries[0].lines) >= 2


def test_save_report_content():
    """Test report formatting with symbol table and statistics."""
    code = "int x = 10; float y = 20.5;"
    res = run_lexer(code)
    assert res.success
    parsed = parse_lexer_output(res.raw_output)
    stats = calculate_statistics(parsed.tokens, parsed.errors)
    sym_table = parsed.get_symbol_table()

    report = format_save_report(code, parsed.tokens, stats, parsed.errors, sym_table)

    assert "C-LANGUAGE COMPILER TOKENIZER" in report
    assert "STATISTICS BREAKDOWN" in report
    assert "ORDERED TOKEN STREAM" in report
    assert "SYMBOL TABLE" in report
    assert "Keywords" in report
    assert "No lexical errors detected" in report
