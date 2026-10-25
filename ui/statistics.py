"""Token Statistics Module for C-Language Compiler Tokenizer.

Computes categorized statistics from parsed tokens and formats complete
exportable analysis reports, including symbol tables and lexical error diagnostics.
"""

from dataclasses import dataclass
from typing import List
from ui.token_parser import (
    Token,
    KEYWORD_TYPES,
    LITERAL_TYPES,
    OPERATOR_TYPES,
    PUNCTUATOR_TYPES,
    PREPROCESSOR_TYPES,
    COMMENT_TYPES,
    SymbolTableEntry,
)


@dataclass
class TokenStatistics:
    """Categorized counts for C-language lexical analysis results."""
    total_tokens: int = 0
    keywords: int = 0
    identifiers: int = 0
    literals: int = 0
    operators: int = 0
    punctuators: int = 0
    comments: int = 0
    preprocessors: int = 0
    errors: int = 0


def calculate_statistics(tokens: List[Token], errors: List[Token]) -> TokenStatistics:
    """Calculate categorized token statistics.

    Args:
        tokens: Full list of parsed Token objects.
        errors: List of error Token objects.

    Returns:
        TokenStatistics object with counts for each compiler category.
    """
    keywords = 0
    identifiers = 0
    literals = 0
    operators = 0
    punctuators = 0
    comments = 0
    preprocessors = 0

    for token in tokens:
        if token.is_error:
            continue
        ttype = token.token_type
        if ttype in KEYWORD_TYPES:
            keywords += 1
        elif ttype == "IDENTIFIER":
            identifiers += 1
        elif ttype in LITERAL_TYPES:
            literals += 1
        elif ttype in OPERATOR_TYPES:
            operators += 1
        elif ttype in PUNCTUATOR_TYPES:
            punctuators += 1
        elif ttype in PREPROCESSOR_TYPES:
            preprocessors += 1
        elif ttype in COMMENT_TYPES:
            comments += 1

    valid_count = (
        keywords
        + identifiers
        + literals
        + operators
        + punctuators
        + comments
        + preprocessors
    )
    error_count = len(errors)

    return TokenStatistics(
        total_tokens=valid_count,
        keywords=keywords,
        identifiers=identifiers,
        literals=literals,
        operators=operators,
        punctuators=punctuators,
        comments=comments,
        preprocessors=preprocessors,
        errors=error_count,
    )


def format_save_report(
    input_text: str,
    tokens: List[Token],
    stats: TokenStatistics,
    errors: List[Token],
    symbol_table: List[SymbolTableEntry] | None = None,
) -> str:
    """Format the full analysis into a clean text report for saving to file.

    Args:
        input_text: The user's input C source code.
        tokens: List of all parsed tokens.
        stats: Computed TokenStatistics.
        errors: List of error tokens.
        symbol_table: Optional list of SymbolTableEntry records.

    Returns:
        Structured string report ready to be written to a .txt file.
    """
    lines = [
        "===========================================================",
        "       C-LANGUAGE COMPILER TOKENIZER & LEXICAL REPORT      ",
        "===========================================================",
        "",
        "SOURCE CODE INPUT",
        "-----------------------------------------------------------",
        input_text.strip(),
        "",
        "STATISTICS BREAKDOWN",
        "-----------------------------------------------------------",
        f"  Total Valid Tokens : {stats.total_tokens}",
        f"  Keywords           : {stats.keywords}",
        f"  Identifiers        : {stats.identifiers}",
        f"  Literals/Constants : {stats.literals}",
        f"  Operators          : {stats.operators}",
        f"  Punctuators        : {stats.punctuators}",
        f"  Comments           : {stats.comments}",
        f"  Preprocessor       : {stats.preprocessors}",
        f"  Lexical Errors     : {stats.errors}",
        "",
        "LEXICAL ERRORS",
        "-----------------------------------------------------------",
    ]

    if errors:
        for err in errors:
            lines.append(f"  [Line {err.line_number}] Token #{err.index}: '{err.lexeme}' -> {err.error_message}")
    else:
        lines.append("  ✓ No lexical errors detected.")

    lines.extend([
        "",
        "ORDERED TOKEN STREAM",
        "-----------------------------------------------------------",
        f"{'#':<5} {'Line':<6} {'Category':<14} {'Token Type':<16} {'Lexeme'}",
        "-" * 65,
    ])

    if tokens:
        for t in tokens:
            status = " [ERROR]" if t.is_error else ""
            lines.append(
                f"{t.index:<5} {t.line_number:<6} {t.category:<14} {t.token_type:<16} {t.lexeme}{status}"
            )
    else:
        lines.append("  (No tokens generated)")

    if symbol_table:
        lines.extend([
            "",
            "SYMBOL TABLE (UNIQUE LEXEMES OVERVIEW)",
            "-----------------------------------------------------------",
            f"{'Category':<14} {'Token Type':<16} {'Count':<7} {'Lines':<12} {'Lexeme'}",
            "-" * 65,
        ])
        for entry in symbol_table:
            lines_str = ",".join(str(l) for l in entry.lines[:8])
            if len(entry.lines) > 8:
                lines_str += "..."
            lines.append(
                f"{entry.category:<14} {entry.token_type:<16} {entry.count:<7} {lines_str:<12} {entry.lexeme}"
            )

    lines.append("")
    return "\n".join(lines)
