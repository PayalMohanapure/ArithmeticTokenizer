"""Styles and Visual Theme for Arithmetic Expression Tokenizer.

Provides a clean, professional dark slate developer-tool aesthetic suitable
for compiler/system software academic demonstrations and viva presentations.
"""

# Color Palette Constants
COLOR_BG_DARK = "#0b0f19"         # Deepest background
COLOR_PANEL_BG = "#111827"        # Panel / Card background
COLOR_PANEL_ALT = "#1f2937"       # Secondary panel / input background
COLOR_BORDER = "#374151"          # Border gray
COLOR_BORDER_FOCUS = "#3b82f6"    # Primary focus border

COLOR_TEXT_PRIMARY = "#f9fafb"    # Bright text
COLOR_TEXT_SECONDARY = "#9ca3af"  # Subtitle / secondary text
COLOR_TEXT_MUTED = "#6b7280"      # Placeholder / disabled text

# Semantic Accents
COLOR_ACCENT_PRIMARY = "#2563eb"  # Primary blue
COLOR_ACCENT_HOVER = "#1d4ed8"    # Primary hover
COLOR_ACCENT_ACTIVE = "#1e40af"   # Primary active

COLOR_SUCCESS = "#10b981"         # Green
COLOR_SUCCESS_BG = "#064e3b"      # Dark green background
COLOR_SUCCESS_BORDER = "#059669"

COLOR_ERROR = "#ef4444"           # Red
COLOR_ERROR_BG = "#450a0a"        # Dark red background
COLOR_ERROR_BORDER = "#dc2626"

COLOR_WARNING = "#f59e0b"         # Amber
COLOR_INFO = "#06b6d4"            # Cyan

# Typography
FONT_FAMILY_UI = "'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif"
FONT_FAMILY_MONO = "'Cascadia Code', 'Consolas', 'Fira Code', 'Courier New', monospace"


GLOBAL_STYLESHEET = f"""
/* Global Window Styling */
QMainWindow, QWidget#centralWidget {{
    background-color: {COLOR_BG_DARK};
    color: {COLOR_TEXT_PRIMARY};
    font-family: {FONT_FAMILY_UI};
    font-size: 13px;
}}

/* Scrollbars */
QScrollBar:vertical {{
    border: none;
    background: #111827;
    width: 8px;
    margin: 0px;
    border-radius: 4px;
}}
QScrollBar::handle:vertical {{
    background: #374151;
    min-height: 20px;
    border-radius: 4px;
}}
QScrollBar::handle:vertical:hover {{
    background: #4b5563;
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}
QScrollBar:horizontal {{
    border: none;
    background: #111827;
    height: 8px;
    margin: 0px;
    border-radius: 4px;
}}
QScrollBar::handle:horizontal {{
    background: #374151;
    min-width: 20px;
    border-radius: 4px;
}}
QScrollBar::handle:horizontal:hover {{
    background: #4b5563;
}}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
    height: 0px;
}}

/* Card Panels */
QFrame.cardPanel {{
    background-color: {COLOR_PANEL_BG};
    border: 1px solid {COLOR_BORDER};
    border-radius: 8px;
}}

/* Section Headers */
QLabel.sectionHeader {{
    color: {COLOR_TEXT_PRIMARY};
    font-size: 13px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}}

QLabel.subHeader {{
    color: {COLOR_TEXT_SECONDARY};
    font-size: 12px;
}}

/* Multiline Expression Editor */
QPlainTextEdit#expressionEditor {{
    background-color: #0d131f;
    color: #e2e8f0;
    font-family: {FONT_FAMILY_MONO};
    font-size: 14px;
    line-height: 1.5;
    border: 1px solid {COLOR_BORDER};
    border-radius: 6px;
    padding: 10px 12px;
    selection-background-color: #2563eb;
    selection-color: #ffffff;
}}
QPlainTextEdit#expressionEditor:focus {{
    border: 1px solid {COLOR_BORDER_FOCUS};
}}

/* Action Buttons */
QPushButton {{
    font-family: {FONT_FAMILY_UI};
    font-size: 13px;
    font-weight: 600;
    padding: 8px 16px;
    border-radius: 6px;
    border: 1px solid {COLOR_BORDER};
    background-color: {COLOR_PANEL_ALT};
    color: {COLOR_TEXT_PRIMARY};
}}
QPushButton:hover {{
    background-color: #374151;
    border-color: #4b5563;
}}
QPushButton:pressed {{
    background-color: #111827;
}}

/* Primary Action: Tokenize Button */
QPushButton#tokenizeButton {{
    background-color: {COLOR_ACCENT_PRIMARY};
    border: 1px solid #3b82f6;
    color: #ffffff;
    font-size: 13px;
    font-weight: 700;
    padding: 8px 22px;
}}
QPushButton#tokenizeButton:hover {{
    background-color: {COLOR_ACCENT_HOVER};
    border-color: #60a5fa;
}}
QPushButton#tokenizeButton:pressed {{
    background-color: {COLOR_ACCENT_ACTIVE};
}}

/* Clear Button */
QPushButton#clearButton:hover {{
    background-color: #7f1d1d;
    border-color: #ef4444;
    color: #fca5a5;
}}

/* ComboBox for Sample Selector */
QComboBox {{
    background-color: {COLOR_PANEL_ALT};
    color: {COLOR_TEXT_PRIMARY};
    border: 1px solid {COLOR_BORDER};
    border-radius: 6px;
    padding: 6px 12px;
    font-size: 12px;
    min-width: 180px;
}}
QComboBox:hover {{
    border-color: #4b5563;
}}
QComboBox:focus {{
    border-color: {COLOR_BORDER_FOCUS};
}}
QComboBox::drop-down {{
    border: none;
    width: 24px;
}}
QComboBox QAbstractItemView {{
    background-color: {COLOR_PANEL_BG};
    color: {COLOR_TEXT_PRIMARY};
    border: 1px solid {COLOR_BORDER};
    selection-background-color: {COLOR_ACCENT_PRIMARY};
    selection-color: #ffffff;
    padding: 4px;
}}

/* Token Table */
QTableWidget#tokenTable {{
    background-color: #0d131f;
    alternate-background-color: #111827;
    border: 1px solid {COLOR_BORDER};
    border-radius: 6px;
    gridline-color: #1f2937;
    color: {COLOR_TEXT_PRIMARY};
    font-size: 13px;
    selection-background-color: #1e3a8a;
    selection-color: #ffffff;
}}
QTableWidget#tokenTable::item {{
    padding: 6px 10px;
    border-bottom: 1px solid #1a2234;
}}
QHeaderView::section {{
    background-color: #131c2e;
    color: {COLOR_TEXT_SECONDARY};
    font-family: {FONT_FAMILY_UI};
    font-weight: 600;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    padding: 8px 10px;
    border: none;
    border-bottom: 1px solid {COLOR_BORDER};
}}

/* Stat Cards */
QFrame.statCard {{
    background-color: #0d131f;
    border: 1px solid #1f2937;
    border-radius: 6px;
    padding: 8px 10px;
}}
QLabel.statValue {{
    font-family: {FONT_FAMILY_MONO};
    font-size: 20px;
    font-weight: 700;
    color: #38bdf8;
}}
QLabel.statLabel {{
    font-size: 11px;
    font-weight: 600;
    color: {COLOR_TEXT_SECONDARY};
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}

/* Error Panel */
QFrame.errorPanelNoErrors {{
    background-color: #064e3b;
    border: 1px solid #059669;
    border-radius: 6px;
    padding: 8px 12px;
}}
QFrame.errorPanelHasErrors {{
    background-color: #450a0a;
    border: 1px solid #dc2626;
    border-radius: 6px;
    padding: 8px 12px;
}}

/* Token Legend / Help Card */
QFrame.legendPanel {{
    background-color: #0d131f;
    border: 1px solid #1f2937;
    border-radius: 6px;
    padding: 10px;
}}

/* Status Bar */
QStatusBar {{
    background-color: {COLOR_BG_DARK};
    color: {COLOR_TEXT_SECONDARY};
    font-size: 12px;
    border-top: 1px solid #1f2937;
}}
"""


def get_token_type_badge_color(token_type: str) -> tuple[str, str]:
    """Return (background_color, text_color) for a given token type."""
    colors = {
        "IDENTIFIER": ("#0c4a6e", "#38bdf8"),    # Sky blue
        "INTEGER": ("#78350f", "#fbbf24"),       # Amber
        "FLOAT": ("#854d0e", "#fde047"),         # Yellow
        "PLUS": ("#581c87", "#c084fc"),          # Purple
        "MINUS": ("#581c87", "#c084fc"),
        "MULTIPLY": ("#581c87", "#c084fc"),
        "DIVIDE": ("#581c87", "#c084fc"),
        "MODULO": ("#581c87", "#c084fc"),
        "POWER": ("#581c87", "#c084fc"),
        "ASSIGN": ("#1e3a8a", "#93c5fd"),        # Blue
        "LPAREN": ("#064e3b", "#34d399"),        # Emerald
        "RPAREN": ("#064e3b", "#34d399"),
        "ERROR": ("#7f1d1d", "#f87171"),         # Red
    }
    return colors.get(token_type, ("#1f2937", "#9ca3af"))
