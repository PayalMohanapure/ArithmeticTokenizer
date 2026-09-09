"""Lexer Runner Module.

Executes the existing compiled FLEX tokenizer binary (lexer.exe) via safe
subprocess stdin/stdout piping without invoking shell or implementing any
tokenization in Python.
"""

import os
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class LexerResult:
    """Represents the execution outcome of the FLEX lexer binary."""
    success: bool
    raw_output: str
    error_message: str
    return_code: int


def find_lexer_executable(custom_path: Optional[str] = None) -> Optional[Path]:
    """Locate the lexer.exe binary dynamically across candidate locations."""
    if custom_path is not None:
        custom_candidate = Path(custom_path).resolve()
        if custom_candidate.is_file() and os.access(custom_candidate, os.X_OK | os.R_OK):
            return custom_candidate
        return None

    candidates = [
        # Standard location: project root when running from ui/
        Path(__file__).resolve().parent.parent / "lexer.exe",
        # Current working directory
        Path.cwd() / "lexer.exe",
        # Inside ui/ folder (if placed alongside)
        Path(__file__).resolve().parent / "lexer.exe",
    ]

    for candidate in candidates:
        if candidate.is_file() and os.access(candidate, os.X_OK | os.R_OK):
            return candidate

    return None


def run_lexer(expression: str, lexer_path: Optional[str] = None, timeout: float = 5.0) -> LexerResult:
    """Execute lexer.exe with the provided arithmetic expression via stdin.

    Args:
        expression: The raw arithmetic expression text to tokenize.
        lexer_path: Optional path to lexer.exe binary.
        timeout: Maximum seconds to wait for execution before terminating.

    Returns:
        LexerResult with execution status, raw stdout, and diagnostic messages.
    """
    resolved_path = find_lexer_executable(lexer_path)
    if not resolved_path:
        return LexerResult(
            success=False,
            raw_output="",
            error_message=(
                "FLEX tokenizer executable not found.\n\n"
                "Please ensure lexer.exe is present in the project directory."
            ),
            return_code=-1,
        )

    # Normalize CRLF and CR to standard LF so Windows line-endings
    # do not match the '.' catch-all rule in FLEX.
    normalized = expression.replace("\r\n", "\n").replace("\r", "\n")
    if not normalized.endswith("\n"):
        normalized += "\n"

    input_bytes = normalized.encode("utf-8")

    try:
        proc = subprocess.Popen(
            [str(resolved_path)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False,
        )
        stdout_bytes, stderr_bytes = proc.communicate(input=input_bytes, timeout=timeout)
        stdout_str = stdout_bytes.decode("utf-8", errors="replace")
        stderr_str = stderr_bytes.decode("utf-8", errors="replace").strip()

        return LexerResult(
            success=True,
            raw_output=stdout_str,
            error_message=stderr_str,
            return_code=proc.returncode,
        )

    except subprocess.TimeoutExpired:
        proc.kill()
        try:
            proc.communicate()
        except Exception:
            pass
        return LexerResult(
            success=False,
            raw_output="",
            error_message=f"Lexer execution timed out after {timeout} seconds.",
            return_code=-1,
        )

    except Exception as exc:
        return LexerResult(
            success=False,
            raw_output="",
            error_message=f"Failed to execute lexer: {exc}",
            return_code=-1,
        )
