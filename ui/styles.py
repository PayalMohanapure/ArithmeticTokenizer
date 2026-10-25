"""Styles and Visual Theme for C-Language Compiler Tokenizer.

Provides a clean, professional dark slate developer-tool aesthetic suitable
for compiler/system software academic demonstrations and viva presentations.
"""

# Color Palette Constants
COLOR_BG_DARK = "#0a0e17"         # Deepest background
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

/* Multiline Code Editor */
QPlainTextEdit#expressionEditor {{
    background-color: #0b1120;
    color: #e2e8f0;
    font-family: {FONT_FAMILY_MONO};
    font-size: 13px;
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
    padding: 7px 15px;
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
    padding: 7px 20px;
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
    min-width: 250px;
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

/* Tables (Token Table & Symbol Table) */
QTableWidget {{
    background-color: #0b1120;
    alternate-background-color: #111827;
    border: 1px solid {COLOR_BORDER};
    border-radius: 6px;
    gridline-color: #1f2937;
    color: {COLOR_TEXT_PRIMARY};
    font-size: 12px;
    selection-background-color: #1e3a8a;
    selection-color: #ffffff;
}}
QTableWidget::item {{
    padding: 5px 8px;
    border-bottom: 1px solid #1a2234;
}}
QHeaderView::section {{
    background-color: #131c2e;
    color: {COLOR_TEXT_SECONDARY};
    font-family: {FONT_FAMILY_UI};
    font-weight: 700;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    padding: 7px 8px;
    border: none;
    border-bottom: 1px solid {COLOR_BORDER};
}}

/* Stat Cards */
QFrame.statCard {{
    background-color: #0b1120;
    border: 1px solid #1f2937;
    border-radius: 6px;
    padding: 8px 10px;
}}
QLabel.statValue {{
    font-family: {FONT_FAMILY_MONO};
    font-size: 18px;
    font-weight: 700;
    color: #38bdf8;
}}
QLabel.statLabel {{
    font-size: 10px;
    font-weight: 700;
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

/* QTabWidget Navigator Styling */
QTabWidget::pane {{
    border: 1px solid {COLOR_BORDER};
    border-radius: 6px;
    background-color: {COLOR_PANEL_BG};
    top: -1px;
}}
QTabBar::tab {{
    background-color: #0f172a;
    color: {COLOR_TEXT_SECONDARY};
    padding: 7px 14px;
    font-weight: 600;
    font-size: 12px;
    border: 1px solid {COLOR_BORDER};
    border-bottom: none;
    border-top-left-radius: 5px;
    border-top-right-radius: 5px;
    margin-right: 2px;
}}
QTabBar::tab:selected {{
    background-color: {COLOR_PANEL_BG};
    color: #38bdf8;
    border-bottom: 2px solid #38bdf8;
}}
QTabBar::tab:hover:!selected {{
    background-color: #1e293b;
    color: {COLOR_TEXT_PRIMARY};
}}

/* Status Bar */
QStatusBar {{
    background-color: {COLOR_BG_DARK};
    color: {COLOR_TEXT_SECONDARY};
    font-size: 12px;
    border-top: 1px solid #1f2937;
}}
"""


def get_token_type_badge_color(token_type: str, category: str = "") -> tuple[str, str]:
    """Return (background_color, text_color) for a given token type or category."""
    colors = {
        # Keywords
        "KEYWORD": ("#7c2d12", "#fdba74"),         # Warm Amber / Orange
        # Identifiers
        "IDENTIFIER": ("#0c4a6e", "#38bdf8"),      # Sky Blue
        # Literals
        "INTEGER": ("#78350f", "#fbbf24"),         # Amber
        "FLOAT": ("#854d0e", "#fde047"),           # Yellow
        "STRING_LITERAL": ("#064e3b", "#34d399"),  # Emerald Green
        "CHAR_LITERAL": ("#065f46", "#6ee7b7"),    # Teal Green
        # Arithmetic Operators
        "PLUS": ("#581c87", "#c084fc"),            # Purple
        "MINUS": ("#581c87", "#c084fc"),
        "MULTIPLY": ("#581c87", "#c084fc"),
        "DIVIDE": ("#581c87", "#c084fc"),
        "MODULO": ("#581c87", "#c084fc"),
        "POWER": ("#581c87", "#c084fc"),
        # Assignment Operators
        "ASSIGN": ("#1e3a8a", "#93c5fd"),          # Blue
        "ADD_ASSIGN": ("#1e3a8a", "#93c5fd"),
        "SUB_ASSIGN": ("#1e3a8a", "#93c5fd"),
        "MUL_ASSIGN": ("#1e3a8a", "#93c5fd"),
        "DIV_ASSIGN": ("#1e3a8a", "#93c5fd"),
        "MOD_ASSIGN": ("#1e3a8a", "#93c5fd"),
        # Inc / Dec
        "INC_OP": ("#4c1d95", "#a78bfa"),          # Violet
        "DEC_OP": ("#4c1d95", "#a78bfa"),
        # Relational Operators
        "LT_OP": ("#115e59", "#2dd4bf"),           # Teal
        "GT_OP": ("#115e59", "#2dd4bf"),
        "LE_OP": ("#115e59", "#2dd4bf"),
        "GE_OP": ("#115e59", "#2dd4bf"),
        "EQ_OP": ("#115e59", "#2dd4bf"),
        "NE_OP": ("#115e59", "#2dd4bf"),
        # Logical Operators
        "LOGICAL_AND": ("#134e4a", "#5eead4"),     # Bright Teal
        "LOGICAL_OR": ("#134e4a", "#5eead4"),
        "LOGICAL_NOT": ("#134e4a", "#5eead4"),
        # Bitwise Operators
        "BIT_AND": ("#312e81", "#a5b4fc"),         # Indigo
        "BIT_OR": ("#312e81", "#a5b4fc"),
        "BIT_XOR": ("#312e81", "#a5b4fc"),
        "BIT_NOT": ("#312e81", "#a5b4fc"),
        "LEFT_SHIFT": ("#312e81", "#a5b4fc"),
        "RIGHT_SHIFT": ("#312e81", "#a5b4fc"),
        # Member / Pointer
        "ARROW": ("#3b0764", "#e9d5ff"),
        "DOT": ("#3b0764", "#e9d5ff"),
        # Conditional
        "QUESTION": ("#831843", "#f472b6"),
        "COLON": ("#831843", "#f472b6"),
        # Punctuators
        "LPAREN": ("#1e293b", "#cbd5e1"),          # Slate
        "RPAREN": ("#1e293b", "#cbd5e1"),
        "LBRACE": ("#1e293b", "#cbd5e1"),
        "RBRACE": ("#1e293b", "#cbd5e1"),
        "LBRACKET": ("#1e293b", "#cbd5e1"),
        "RBRACKET": ("#1e293b", "#cbd5e1"),
        "SEMICOLON": ("#1e293b", "#cbd5e1"),
        "COMMA": ("#1e293b", "#cbd5e1"),
        # Preprocessor
        "PREPROCESSOR": ("#831843", "#f472b6"),    # Pink
        "HEADER_FILE": ("#701a75", "#f0abfc"),     # Fuchsia
        # Comments
        "COMMENT": ("#1e293b", "#94a3b8"),         # Dim Muted Gray
        # Errors
        "ERROR": ("#7f1d1d", "#f87171"),           # Red
    }

    if token_type in colors:
        return colors[token_type]

    # Category fallback
    cat_colors = {
        "Keyword": ("#7c2d12", "#fdba74"),
        "Identifier": ("#0c4a6e", "#38bdf8"),
        "Literal": ("#78350f", "#fbbf24"),
        "Operator": ("#581c87", "#c084fc"),
        "Punctuator": ("#1e293b", "#cbd5e1"),
        "Preprocessor": ("#831843", "#f472b6"),
        "Comment": ("#1e293b", "#94a3b8"),
        "Error": ("#7f1d1d", "#f87171"),
    }
    return cat_colors.get(category, ("#1f2937", "#9ca3af"))
