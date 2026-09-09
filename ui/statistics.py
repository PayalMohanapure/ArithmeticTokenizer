"""Token Statistics Module.

Computes categorized statistics from parsed tokens and formats complete
exportable analysis reports.
"""

from dataclasses import dataclass
from typing import List
from ui.token_parser import Token


NUMBER_TYPES = {"INTEGER", "FLOAT"}
OPERATOR_TYPES = {
    "PLUS",
    "MINUS",
    "MULTIPLY",
    "DIVIDE",
    "MODULO",
    "POWER",
    "ASSIGN",
}
PARENTHESIS_TYPES = {"LPAREN", "RPAREN"}
IDENTIFIER_TYPES = {"IDENTIFIER"}


@dataclass
class TokenStatistics:
    """Categorized counts for lexical analysis results."""
    total_tokens: int = 0
    identifiers: int = 0
    numbers: int = 0
    operators: int = 0
    parentheses: int = 0
    errors: int = 0


def calculate_statistics(tokens: List[Token], errors: List[Token]) -> TokenStatistics:
    """Calculate categorized token statistics.

    Args:
        tokens: Full list of parsed Token objects (valid tokens).
        errors: List of error Token objects.

    Returns:
        TokenStatistics object with counts for each category.
    """
    identifiers = 0
    numbers = 0
    operators = 0
    parentheses = 0

    for token in tokens:
        if token.is_error:
            continue
        ttype = token.token_type
        if ttype in IDENTIFIER_TYPES:
            identifiers += 1
        elif ttype in NUMBER_TYPES:
            numbers += 1
        elif ttype in OPERATOR_TYPES:
            operators += 1
        elif ttype in PARENTHESIS_TYPES:
            parentheses += 1

    valid_count = identifiers + numbers + operators + parentheses
    error_count = len(errors)

    return TokenStatistics(
        total_tokens=valid_count,
        identifiers=identifiers,
        numbers=numbers,
        operators=operators,
        parentheses=parentheses,
        errors=error_count,
    )


def format_save_report(
    input_text: str,
    tokens: List[Token],
    stats: TokenStatistics,
    errors: List[Token],
) -> str:
    """Format the full analysis into a clean text report for saving to file.

    Args:
        input_text: The user's input arithmetic expression.
        tokens: List of all parsed tokens.
        stats: Computed TokenStatistics.
        errors: List of error tokens.

    Returns:
        Structured string report ready to be written to a .txt file.
    """
    lines = [
        "ARITHMETIC EXPRESSION TOKENIZER",
        "===============================",
        "",
        "INPUT",
        "-----",
        input_text.strip(),
        "",
        "TOKENS",
        "------",
    ]

    if tokens:
        for t in tokens:
            status = f" (Error: {t.error_message})" if t.is_error else ""
            lines.append(f"{t.index}. {t.lexeme:<12} {t.token_type}{status}")
    else:
        lines.append("(No tokens generated)")

    lines.extend([
        "",
        "STATISTICS",
        "----------",
        f"Total Tokens: {stats.total_tokens}",
        f"Identifiers: {stats.identifiers}",
        f"Numbers: {stats.numbers}",
        f"Operators: {stats.operators}",
        f"Parentheses: {stats.parentheses}",
        f"Errors: {stats.errors}",
        "",
        "ERRORS",
        "------",
    ])

    if errors:
        for err in errors:
            lines.append(f"• {err.lexeme}  →  {err.error_message}")
    else:
        lines.append("No lexical errors detected.")

    lines.append("")
    return "\n".join(lines)
