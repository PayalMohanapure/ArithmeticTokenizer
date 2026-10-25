"""Main Window for C-Language Compiler Tokenizer Desktop UI.

Implements a modern, academic compiler-design GUI using PySide6.
Features multi-line C code testing, categorized token streams, tabbed navigator,
lexical error diagnostics, and a consolidated Symbol Table overview.
"""

from pathlib import Path
from typing import List

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor, QBrush
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QPlainTextEdit,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QComboBox,
    QFileDialog,
    QMessageBox,
    QFrame,
    QSplitter,
    QStatusBar,
    QGridLayout,
    QTabWidget,
    QLineEdit,
)

from ui.lexer_runner import run_lexer, find_lexer_executable
from ui.token_parser import parse_lexer_output, Token, SymbolTableEntry
from ui.statistics import (
    calculate_statistics,
    format_save_report,
    TokenStatistics,
)
from ui.styles import (
    GLOBAL_STYLESHEET,
    FONT_FAMILY_MONO,
    get_token_type_badge_color,
)


SAMPLE_TEST_CASES = [
    ("Select a C code test case...", ""),
    (
        "1. Arithmetic Operators & Expressions",
        """// 1. Arithmetic Operators & Precedence
int main() {
    int a = 15;
    int b = 4;
    float result = (a + b) * 2.5 - (a / b);
    int remainder = a % b;
    a += 5;
    b *= 2;
    return 0;
}""",
    ),
    (
        "2. If - Else Conditional Statements",
        """// 2. Conditional Branching (if, else if, else)
int main() {
    int score = 85;
    if (score >= 90) {
        printf("Grade: A\\n");
    } else if (score >= 75 && score < 90) {
        printf("Grade: B\\n");
    } else if (score >= 50 && score < 75) {
        printf("Grade: C\\n");
    } else {
        printf("Grade: F\\n");
    }
    return 0;
}""",
    ),
    (
        "3. Do - While Loop Construct",
        """// 3. Do-While Iteration Construct
int main() {
    int count = 1;
    int sum = 0;
    do {
        sum += count;
        count++;
    } while (count <= 10);
    printf("Total sum: %d\\n", sum);
    return 0;
}""",
    ),
    (
        "4. For Loop with Step & Accumulation",
        """// 4. For Loop with Initializer, Condition, and Step
int main() {
    int n = 10;
    int factorial = 1;
    for (int i = 1; i <= n; i++) {
        factorial *= i;
    }
    printf("Factorial of %d is %d\\n", n, factorial);
    return 0;
}""",
    ),
    (
        "5. Function Declaration & Invocation",
        """// 5. Function Definition, Parameters, and Return
int calculate_power(int base, int exp) {
    int res = 1;
    for (int i = 0; i < exp; i++) {
        res *= base;
    }
    return res;
}

int main() {
    int ans = calculate_power(2, 8);
    printf("Result: %d\\n", ans);
    return 0;
}""",
    ),
    (
        "6. Switch - Case Multi-way Branching",
        """// 6. Switch-Case Statement with Default and Break
int main() {
    int option = 2;
    switch (option) {
        case 1:
            printf("Choice: Add\\n");
            break;
        case 2:
            printf("Choice: Subtract\\n");
            break;
        case 3:
            printf("Choice: Multiply\\n");
            break;
        default:
            printf("Invalid Option\\n");
            break;
    }
    return 0;
}""",
    ),
    (
        "7. Nested Loops (Pattern Generation)",
        """// 7. Nested For Loops (Multi-dimensional)
int main() {
    int rows = 4;
    for (int i = 1; i <= rows; i++) {
        for (int j = 1; j <= i; j++) {
            printf("* ");
        }
        printf("\\n");
    }
    return 0;
}""",
    ),
    (
        "8. Struct Definition & Pointer Member Access",
        """// 8. Structures, Pointers, and Member Access (., ->)
struct Student {
    int id;
    float gpa;
};

int main() {
    struct Student s1;
    s1.id = 101;
    s1.gpa = 3.85;

    struct Student *ptr = &s1;
    printf("ID: %d, GPA: %.2f\\n", ptr->id, ptr->gpa);
    return 0;
}""",
    ),
    (
        "9. Preprocessor Directives & Macro Constants",
        """// 9. Preprocessor Macros, Includes, and Constants
#include <stdio.h>
#define MAX_BUFFER 1024
#define PI 3.14159

int main() {
    const float radius = 7.5;
    float circumference = 2.0 * PI * radius;
    printf("Circumference: %f\\n", circumference);
    return 0;
}""",
    ),
    (
        "10. While Loop with Break and Continue",
        """// 10. While Loop Control Flow (break & continue)
int main() {
    int num = 0;
    while (num < 20) {
        num++;
        if (num % 2 == 0) {
            continue; // skip evens
        }
        if (num > 15) {
            break;    // terminate early
        }
        printf("Odd: %d\\n", num);
    }
    return 0;
}""",
    ),
    (
        "11. Array Operations & Sizeof Operator",
        """// 11. Array Declaration, Subscripts, and sizeof()
int main() {
    int numbers[5] = {10, 20, 30, 40, 50};
    int total_elements = sizeof(numbers) / sizeof(numbers[0]);
    for (int i = 0; i < total_elements; i++) {
        printf("Element[%d] = %d\\n", i, numbers[i]);
    }
    return 0;
}""",
    ),
    (
        "12. Ternary Operator & Complex Logical Expressions",
        """// 12. Ternary Operator (?:) and Boolean Logic (&&, ||, !)
int main() {
    int x = 25, y = 40;
    int max_val = (x > y) ? x : y;
    int is_valid = (x != 0 && y != 0) || !(x < 10);
    printf("Max: %d, Valid: %d\\n", max_val, is_valid);
    return 0;
}""",
    ),
    (
        "13. ⚠ Lexical Errors Demonstration",
        """// 13. Lexical Error Cases (Contains invalid characters: @, $, `, #)
int main() {
    int normal_var = 10;
    float invalid$var = 3.14; // $ is invalid in standard C
    int result = normal_var @ 20; // @ is invalid operator
    int `quoted` = 99; // backticks are invalid in C
    printf("Value: %d", normal_var);
    return 0;
}""",
    ),
    (
        "14. Comments (Single-Line & Multi-Line)",
        """/* 
   Compiler Tokenizer Test
   Multi-Line Comment Block
*/
#include <stdio.h>

// Single-line comment before function
int main() {
    int active = 1; // inline single-line comment
    /* inline multi-line comment */
    char letter = 'Z';
    char greeting[] = "Hello, Lexer!";
    return 0;
}""",
    ),
    (
        "15. Complete Comprehensive Program (All Constructs)",
        """// 15. Comprehensive C Program with All Language Features
#include <stdio.h>
#define LIMIT 50

int is_prime(int n) {
    if (n <= 1) return 0;
    for (int i = 2; i * i <= n; i++) {
        if (n % i == 0) return 0;
    }
    return 1;
}

int main() {
    int count = 0;
    printf("Primes up to %d:\\n", LIMIT);

    for (int num = 2; num <= LIMIT; num++) {
        if (is_prime(num)) {
            printf("%d ", num);
            count++;
        }
    }

    printf("\\nTotal primes found: %d\\n", count);
    return 0;
}""",
    ),
]


class MainWindow(QMainWindow):
    """Main Application Window for C-Language Compiler Tokenizer."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("C-Language Compiler Tokenizer — Lexical Analysis & Symbol Table using FLEX")
        self.resize(1200, 820)
        self.setMinimumSize(960, 650)

        # State
        self.current_tokens: List[Token] = []
        self.current_errors: List[Token] = []
        self.current_stats: TokenStatistics = TokenStatistics()
        self.current_symbol_table: List[SymbolTableEntry] = []

        # Apply Global Styling
        self.setStyleSheet(GLOBAL_STYLESHEET)

        # Setup UI Components
        self._init_ui()
        self._check_engine_status()

    def _init_ui(self) -> None:
        """Construct all UI sections, panels, and layouts."""
        central_widget = QWidget(self)
        central_widget.setObjectName("centralWidget")
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(16, 14, 16, 10)
        main_layout.setSpacing(12)

        # 1. Header Section
        header_widget = self._create_header()
        main_layout.addWidget(header_widget)

        # 2. Code Input & Controls Card
        input_card = self._create_input_card()
        main_layout.addWidget(input_card)

        # 3. Main Workspace Splitter (Token Stream on Left, Navigator/Overview on Right)
        workspace_splitter = QSplitter(Qt.Horizontal)
        workspace_splitter.setChildrenCollapsible(False)

        # Left Panel: All Tokens Stream Table
        table_panel = self._create_stream_panel()
        workspace_splitter.addWidget(table_panel)

        # Right Panel: Navigator Tabs (Statistics, Symbol Table, Category Views, Errors, Reference)
        navigator_panel = self._create_navigator_panel()
        workspace_splitter.addWidget(navigator_panel)

        # Balanced splitter proportions (52% left stream, 48% right navigator)
        workspace_splitter.setStretchFactor(0, 52)
        workspace_splitter.setStretchFactor(1, 48)

        main_layout.addWidget(workspace_splitter, stretch=1)

        # 4. Status Bar
        self.status_bar = QStatusBar(self)
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("● Ready — Select a C test case or enter source code to begin lexical analysis")

    def _create_header(self) -> QWidget:
        """Create the top title and engine status bar."""
        header = QFrame()
        layout = QHBoxLayout(header)
        layout.setContentsMargins(0, 0, 0, 0)

        title_box = QVBoxLayout()
        title_box.setSpacing(2)

        title_label = QLabel("C-LANGUAGE COMPILER TOKENIZER")
        title_label.setStyleSheet("font-size: 18px; font-weight: 800; color: #f8fafc; letter-spacing: 1px;")
        subtitle_label = QLabel("Compiler Design — Lexical Analysis & Symbol Table Generation using FLEX")
        subtitle_label.setStyleSheet("font-size: 12px; color: #94a3b8; font-weight: 500;")

        title_box.addWidget(title_label)
        title_box.addWidget(subtitle_label)
        layout.addLayout(title_box)

        layout.addStretch()

        # Engine Status Badge
        self.engine_badge = QLabel("● FLEX ENGINE READY")
        self.engine_badge.setStyleSheet(
            "background-color: #064e3b; color: #34d399; font-weight: 700; "
            "font-size: 11px; padding: 6px 12px; border-radius: 12px; border: 1px solid #059669;"
        )
        layout.addWidget(self.engine_badge)

        return header

    def _create_input_card(self) -> QFrame:
        """Create the multi-line C code editor and control actions panel."""
        card = QFrame()
        card.setProperty("class", "cardPanel")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(14, 10, 14, 10)
        card_layout.setSpacing(8)

        # Top row: Label & Test Case Dropdown
        top_row = QHBoxLayout()
        input_label = QLabel("C SOURCE CODE INPUT")
        input_label.setProperty("class", "sectionHeader")
        top_row.addWidget(input_label)

        top_row.addStretch()

        sample_label = QLabel("Test Case:")
        sample_label.setStyleSheet("color: #94a3b8; font-size: 12px; font-weight: 500;")
        top_row.addWidget(sample_label)

        self.sample_combo = QComboBox()
        for label, _ in SAMPLE_TEST_CASES:
            self.sample_combo.addItem(label)
        self.sample_combo.currentIndexChanged.connect(self._on_sample_selected)
        top_row.addWidget(self.sample_combo)

        card_layout.addLayout(top_row)

        # Multiline Code Editor
        self.expression_editor = QPlainTextEdit()
        self.expression_editor.setObjectName("expressionEditor")
        self.expression_editor.setPlaceholderText(
            "Enter C language source code here...\n"
            "(e.g., int main() { int x = 10; return 0; } or select a test case from the dropdown above)"
        )
        self.expression_editor.setFixedHeight(120)
        card_layout.addWidget(self.expression_editor)

        # Action Buttons Row
        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)

        self.tokenize_btn = QPushButton("Tokenize Code")
        self.tokenize_btn.setObjectName("tokenizeButton")
        self.tokenize_btn.setCursor(Qt.PointingHandCursor)
        self.tokenize_btn.clicked.connect(self.on_tokenize)
        btn_row.addWidget(self.tokenize_btn)

        self.open_file_btn = QPushButton("Open File")
        self.open_file_btn.setCursor(Qt.PointingHandCursor)
        self.open_file_btn.clicked.connect(self.on_open_file)
        btn_row.addWidget(self.open_file_btn)

        self.save_results_btn = QPushButton("Save Results")
        self.save_results_btn.setCursor(Qt.PointingHandCursor)
        self.save_results_btn.clicked.connect(self.on_save_results)
        btn_row.addWidget(self.save_results_btn)

        self.clear_btn = QPushButton("Clear")
        self.clear_btn.setObjectName("clearButton")
        self.clear_btn.setCursor(Qt.PointingHandCursor)
        self.clear_btn.clicked.connect(self.on_clear)
        btn_row.addWidget(self.clear_btn)

        btn_row.addStretch()

        # Quick stats preview label
        self.quick_stats_label = QLabel("0 tokens | 0 lines")
        self.quick_stats_label.setStyleSheet("color: #64748b; font-size: 11px; font-weight: 600;")
        btn_row.addWidget(self.quick_stats_label)

        card_layout.addLayout(btn_row)

        return card

    def _create_stream_panel(self) -> QFrame:
        """Create the left-hand panel showing the complete ordered token stream."""
        panel = QFrame()
        panel.setProperty("class", "cardPanel")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(8)

        # Header with Search Filter
        header_layout = QHBoxLayout()
        table_title = QLabel("ALL TOKENS STREAM")
        table_title.setProperty("class", "sectionHeader")
        header_layout.addWidget(table_title)

        header_layout.addStretch()

        self.filter_input = QLineEdit()
        self.filter_input.setPlaceholderText("Filter tokens...")
        self.filter_input.setFixedWidth(160)
        self.filter_input.setStyleSheet(
            "background-color: #1f2937; color: #f9fafb; border: 1px solid #374151; "
            "border-radius: 4px; padding: 4px 8px; font-size: 11px;"
        )
        self.filter_input.textChanged.connect(self._filter_stream_table)
        header_layout.addWidget(self.filter_input)

        self.table_count_label = QLabel("0 tokens")
        self.table_count_label.setStyleSheet("color: #94a3b8; font-size: 12px; font-weight: 600;")
        header_layout.addWidget(self.table_count_label)

        layout.addLayout(header_layout)

        # Token Stream Table Widget: #, Line, Category, Token Type, Lexeme
        self.token_table = QTableWidget(0, 5)
        self.token_table.setObjectName("tokenTable")
        self.token_table.setHorizontalHeaderLabels(["#", "Line", "Category", "Token Type", "Lexeme"])
        self.token_table.verticalHeader().setVisible(False)
        self.token_table.setAlternatingRowColors(True)
        self.token_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.token_table.setEditTriggers(QTableWidget.NoEditTriggers)

        header = self.token_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.Stretch)

        layout.addWidget(self.token_table)
        return panel

    def _create_navigator_panel(self) -> QWidget:
        """Create the right-hand navigator tabs containing Statistics, Symbol Table, and Category breakdowns."""
        self.tab_widget = QTabWidget()

        # Tab 1: Statistics Grid
        stats_tab = self._create_statistics_tab()
        self.tab_widget.addTab(stats_tab, "📊 Statistics")

        # Tab 2: Final Symbol Table Overview
        symbol_tab = self._create_symbol_table_tab()
        self.tab_widget.addTab(symbol_tab, "📋 Final Symbol Table")

        # Tab 3: Keywords
        keywords_tab = self._create_category_tab("Keyword")
        self.tab_widget.addTab(keywords_tab, "🔑 Keywords")

        # Tab 4: Identifiers
        identifiers_tab = self._create_category_tab("Identifier")
        self.tab_widget.addTab(identifiers_tab, "📛 Identifiers")

        # Tab 5: Literals
        literals_tab = self._create_category_tab("Literal")
        self.tab_widget.addTab(literals_tab, "🔢 Literals")

        # Tab 6: Operators
        operators_tab = self._create_category_tab("Operator")
        self.tab_widget.addTab(operators_tab, "⚙️ Operators")

        # Tab 7: Lexical Errors
        errors_tab = self._create_errors_tab()
        self.tab_widget.addTab(errors_tab, "⚠ Lexical Errors")

        # Tab 8: Token Reference Guide
        reference_tab = self._create_legend_tab()
        self.tab_widget.addTab(reference_tab, "📖 Reference")

        return self.tab_widget

    def _create_statistics_tab(self) -> QWidget:
        """Tab containing categorized statistics cards and summary metrics."""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        title = QLabel("LEXICAL STATISTICS BREAKDOWN")
        title.setProperty("class", "sectionHeader")
        layout.addWidget(title)

        grid = QGridLayout()
        grid.setSpacing(8)

        self.stat_widgets = {}
        metrics = [
            ("total_tokens", "Total Valid Tokens", "0", 0, 0),
            ("keywords", "Keywords", "0", 0, 1),
            ("identifiers", "Identifiers", "0", 0, 2),
            ("literals", "Literals / Constants", "0", 1, 0),
            ("operators", "Operators", "0", 1, 1),
            ("punctuators", "Punctuators", "0", 1, 2),
            ("comments", "Comments", "0", 2, 0),
            ("preprocessors", "Preprocessor Directives", "0", 2, 1),
            ("errors", "Lexical Errors", "0", 2, 2),
        ]

        for key, label_text, default_val, row, col in metrics:
            stat_frame = QFrame()
            stat_frame.setProperty("class", "statCard")
            stat_layout = QVBoxLayout(stat_frame)
            stat_layout.setContentsMargins(8, 8, 8, 8)
            stat_layout.setSpacing(2)

            val_label = QLabel(default_val)
            val_label.setProperty("class", "statValue")
            val_label.setAlignment(Qt.AlignCenter)

            lbl = QLabel(label_text)
            lbl.setProperty("class", "statLabel")
            lbl.setAlignment(Qt.AlignCenter)

            stat_layout.addWidget(val_label)
            stat_layout.addWidget(lbl)
            grid.addWidget(stat_frame, row, col)

            self.stat_widgets[key] = val_label

        layout.addLayout(grid)

        # Overview summary text card
        summary_card = QFrame()
        summary_card.setProperty("class", "statCard")
        sum_layout = QVBoxLayout(summary_card)
        sum_layout.setContentsMargins(10, 8, 10, 8)

        self.summary_desc_label = QLabel(
            "Tokenize C code to view detailed metrics and category distributions."
        )
        self.summary_desc_label.setStyleSheet("color: #94a3b8; font-size: 12px; line-height: 1.4;")
        self.summary_desc_label.setWordWrap(True)
        sum_layout.addWidget(self.summary_desc_label)

        layout.addWidget(summary_card)
        layout.addStretch()
        return container

    def _create_symbol_table_tab(self) -> QWidget:
        """Tab showing the consolidated unique Symbol Table overview."""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)

        top_row = QHBoxLayout()
        title = QLabel("COMPILER SYMBOL TABLE OVERVIEW")
        title.setProperty("class", "sectionHeader")
        top_row.addWidget(title)

        top_row.addStretch()
        self.symbol_count_label = QLabel("0 unique entries")
        self.symbol_count_label.setStyleSheet("color: #94a3b8; font-size: 11px; font-weight: 600;")
        top_row.addWidget(self.symbol_count_label)
        layout.addLayout(top_row)

        desc = QLabel("Consolidated view of unique lexemes, classifications, frequency, and occurrence line numbers:")
        desc.setStyleSheet("color: #94a3b8; font-size: 11px;")
        layout.addWidget(desc)

        self.symbol_table_widget = QTableWidget(0, 5)
        self.symbol_table_widget.setHorizontalHeaderLabels(["Lexeme", "Category", "Token Type", "Count", "Lines"])
        self.symbol_table_widget.verticalHeader().setVisible(False)
        self.symbol_table_widget.setAlternatingRowColors(True)
        self.symbol_table_widget.setSelectionBehavior(QTableWidget.SelectRows)
        self.symbol_table_widget.setEditTriggers(QTableWidget.NoEditTriggers)

        sym_hdr = self.symbol_table_widget.horizontalHeader()
        sym_hdr.setSectionResizeMode(0, QHeaderView.Stretch)
        sym_hdr.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        sym_hdr.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        sym_hdr.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        sym_hdr.setSectionResizeMode(4, QHeaderView.ResizeToContents)

        layout.addWidget(self.symbol_table_widget)
        return container

    def _create_category_tab(self, category_name: str) -> QWidget:
        """Generic filtered category viewer tab."""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)

        top_row = QHBoxLayout()
        title = QLabel(f"{category_name.upper()}S OVERVIEW")
        title.setProperty("class", "sectionHeader")
        top_row.addWidget(title)

        top_row.addStretch()
        count_lbl = QLabel("0 items")
        count_lbl.setStyleSheet("color: #94a3b8; font-size: 11px; font-weight: 600;")
        top_row.addWidget(count_lbl)
        layout.addLayout(top_row)

        table = QTableWidget(0, 4)
        table.setHorizontalHeaderLabels(["#", "Line", "Lexeme", "Token Type"])
        table.verticalHeader().setVisible(False)
        table.setAlternatingRowColors(True)
        table.setSelectionBehavior(QTableWidget.SelectRows)
        table.setEditTriggers(QTableWidget.NoEditTriggers)

        h = table.horizontalHeader()
        h.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        h.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        h.setSectionResizeMode(2, QHeaderView.Stretch)
        h.setSectionResizeMode(3, QHeaderView.ResizeToContents)

        layout.addWidget(table)

        # Store widgets dynamically
        setattr(self, f"table_{category_name.lower()}", table)
        setattr(self, f"label_{category_name.lower()}", count_lbl)

        return container

    def _create_errors_tab(self) -> QWidget:
        """Tab showing dedicated lexical error diagnostics."""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)

        title = QLabel("LEXICAL ERRORS & DIAGNOSTICS")
        title.setProperty("class", "sectionHeader")
        layout.addWidget(title)

        self.error_content_frame = QFrame()
        self.error_content_frame.setProperty("class", "errorPanelNoErrors")
        self.error_content_layout = QVBoxLayout(self.error_content_frame)
        self.error_content_layout.setContentsMargins(10, 8, 10, 8)

        self.error_status_label = QLabel("✓ No tokenization errors detected")
        self.error_status_label.setStyleSheet("color: #34d399; font-weight: 600; font-size: 12px;")
        self.error_content_layout.addWidget(self.error_status_label)

        layout.addWidget(self.error_content_frame)

        desc = QLabel("Detailed listing of all unrecognized characters and invalid lexical tokens:")
        desc.setStyleSheet("color: #94a3b8; font-size: 11px;")
        layout.addWidget(desc)

        self.error_table = QTableWidget(0, 4)
        self.error_table.setHorizontalHeaderLabels(["Token #", "Line", "Lexeme", "Diagnostic Message"])
        self.error_table.verticalHeader().setVisible(False)
        self.error_table.setAlternatingRowColors(True)
        self.error_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.error_table.setEditTriggers(QTableWidget.NoEditTriggers)

        h = self.error_table.horizontalHeader()
        h.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        h.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        h.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        h.setSectionResizeMode(3, QHeaderView.Stretch)

        layout.addWidget(self.error_table)
        return container

    def _create_legend_tab(self) -> QWidget:
        """Tab showing the C-Language token classification rules."""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)

        title = QLabel("C TOKEN CLASSIFICATION RULES")
        title.setProperty("class", "sectionHeader")
        layout.addWidget(title)

        desc = QLabel("Authoritative rules recognized by the FLEX lexical analyzer engine:")
        desc.setProperty("class", "subHeader")
        layout.addWidget(desc)

        legend_grid = QGridLayout()
        legend_grid.setSpacing(6)

        rules = [
            ("KEYWORD", "int, if, while, return, struct, sizeof...", "32 C reserved language keywords"),
            ("IDENTIFIER", "main, count, calculate_power, ptr...", "[a-zA-Z_][a-zA-Z0-9_]*"),
            ("INTEGER", "10, 0, 1024, 0x1F", "Decimal digits [0-9]+ and Hexadecimal"),
            ("FLOAT", "3.14, 2.5, 1e-5", "Floating-point [0-9]+\\.[0-9]+ and Scientific"),
            ("STRING_LITERAL", '\"Hello, Lexer!\\n\"', "Enclosed in double quotes with escape sequences"),
            ("CHAR_LITERAL", "'Z', '\\n', '\\0'", "Enclosed in single quotes with escapes"),
            ("ARITHMETIC", "+, -, *, /, %, ^", "Addition, Subtraction, Multiplication, Division, Modulo"),
            ("ASSIGNMENT", "=, +=, -=, *=, /=, %=", "Simple and compound assignment operators"),
            ("RELATIONAL", "<, >, <=, >=, ==, !=", "Comparison and equality operators"),
            ("LOGICAL", "&&, ||, !", "Boolean AND, OR, and NOT"),
            ("BITWISE", "&, |, ^, ~, <<, >>", "Bitwise AND, OR, XOR, NOT, Bit-Shifts"),
            ("INC / DEC", "++, --", "Pre/post increment and decrement operators"),
            ("MEMBER / PTR", "->, .", "Structure member and pointer member access"),
            ("PUNCTUATOR", ";, ,, (, ), {, }, [, ]", "Semicolons, commas, braces, brackets, parentheses"),
            ("PREPROCESSOR", "#include, #define, <stdio.h>", "Directives and standard library header files"),
            ("COMMENTS", "// ..., /* ... */", "Single-line and multi-line comments"),
        ]

        for i, (name, sym, desc_text) in enumerate(rules):
            row = i // 2
            col = (i % 2) * 2

            tag_lbl = QLabel(name)
            bg, fg = get_token_type_badge_color(name)
            tag_lbl.setStyleSheet(
                f"background-color: {bg}; color: {fg}; font-family: {FONT_FAMILY_MONO}; "
                "font-size: 11px; font-weight: 700; padding: 3px 6px; border-radius: 4px;"
            )
            legend_grid.addWidget(tag_lbl, row, col)

            detail_lbl = QLabel(f"<b>{sym}</b> — {desc_text}")
            detail_lbl.setStyleSheet("color: #94a3b8; font-size: 11px;")
            legend_grid.addWidget(detail_lbl, row, col + 1)

        layout.addLayout(legend_grid)
        layout.addStretch()
        return container

    def _check_engine_status(self) -> None:
        """Check if lexer.exe is found and update the engine status badge."""
        exe_path = find_lexer_executable()
        if exe_path:
            self.engine_badge.setText("● FLEX ENGINE READY")
            self.engine_badge.setStyleSheet(
                "background-color: #064e3b; color: #34d399; font-weight: 700; "
                "font-size: 11px; padding: 6px 12px; border-radius: 12px; border: 1px solid #059669;"
            )
            self.engine_badge.setToolTip(f"Located at: {exe_path}")
        else:
            self.engine_badge.setText("● LEXER.EXE MISSING")
            self.engine_badge.setStyleSheet(
                "background-color: #450a0a; color: #f87171; font-weight: 700; "
                "font-size: 11px; padding: 6px 12px; border-radius: 12px; border: 1px solid #dc2626;"
            )
            self.engine_badge.setToolTip("lexer.exe not found in project directory.")

    def _on_sample_selected(self, index: int) -> None:
        """Load a selected sample test case into the code editor and auto-tokenize."""
        if 0 < index < len(SAMPLE_TEST_CASES):
            label, code = SAMPLE_TEST_CASES[index]
            self.expression_editor.setPlainText(code)
            self.status_bar.showMessage(f"● Loaded test case: {label}")
            self.on_tokenize()

    def on_tokenize(self) -> None:
        """Run the FLEX lexer on the input C code and update all views."""
        code_input = self.expression_editor.toPlainText().strip()
        if not code_input:
            QMessageBox.warning(
                self,
                "Empty Code Input",
                "Please enter C source code or select a test case from the dropdown.",
            )
            self.expression_editor.setFocus()
            return

        self._check_engine_status()

        # Run authoritative lexer binary
        result = run_lexer(code_input)
        if not result.success:
            self.status_bar.showMessage("● Tokenization failed")
            QMessageBox.critical(
                self,
                "Lexer Execution Error",
                result.error_message,
            )
            return

        # Parse raw output into structured tokens
        parsed = parse_lexer_output(result.raw_output)
        self.current_tokens = parsed.tokens
        self.current_errors = parsed.errors
        self.current_symbol_table = parsed.get_symbol_table()

        # Calculate statistics
        self.current_stats = calculate_statistics(parsed.tokens, parsed.errors)

        # Update all UI views
        self._populate_stream_table(parsed.tokens)
        self._populate_symbol_table(self.current_symbol_table)
        self._populate_category_tables(parsed.tokens)
        self._update_statistics_view(self.current_stats, len(code_input.splitlines()))
        self._update_errors_view(parsed.errors)

        line_count = len(code_input.splitlines())
        self.quick_stats_label.setText(f"{len(parsed.tokens)} tokens | {line_count} lines")

        if parsed.error_count == 0:
            self.status_bar.showMessage(
                f"● Tokenization completed: {self.current_stats.total_tokens} tokens recognized across {line_count} lines"
            )
        else:
            self.status_bar.showMessage(
                f"● Tokenization completed with {parsed.error_count} lexical error(s)"
            )
            # Switch to Errors tab if errors exist
            self.tab_widget.setCurrentIndex(6)

    def _populate_stream_table(self, tokens: List[Token]) -> None:
        """Populate the left-hand token stream table."""
        self.token_table.setRowCount(0)
        self.token_table.setRowCount(len(tokens))
        self.table_count_label.setText(f"{len(tokens)} token(s)")

        mono_font = QFont("Cascadia Code")
        mono_font.setStyleHint(QFont.Monospace)
        mono_font.setPointSize(10)

        badge_font = QFont()
        badge_font.setBold(True)
        badge_font.setPointSize(9)

        for row, token in enumerate(tokens):
            # Column 0: Index (#)
            item_idx = QTableWidgetItem(str(token.index))
            item_idx.setTextAlignment(Qt.AlignCenter)
            self.token_table.setItem(row, 0, item_idx)

            # Column 1: Line Number
            item_line = QTableWidgetItem(str(token.line_number))
            item_line.setTextAlignment(Qt.AlignCenter)
            self.token_table.setItem(row, 1, item_line)

            # Column 2: Category Badge
            item_cat = QTableWidgetItem(token.category)
            item_cat.setTextAlignment(Qt.AlignCenter)
            bg, fg = get_token_type_badge_color(token.token_type, token.category)
            item_cat.setBackground(QBrush(QColor(bg)))
            item_cat.setForeground(QBrush(QColor(fg)))
            item_cat.setFont(badge_font)
            self.token_table.setItem(row, 2, item_cat)

            # Column 3: Token Type
            item_type = QTableWidgetItem(token.token_type)
            item_type.setTextAlignment(Qt.AlignCenter)
            item_type.setForeground(QBrush(QColor("#cbd5e1")))
            self.token_table.setItem(row, 3, item_type)

            # Column 4: Lexeme
            item_lex = QTableWidgetItem(token.lexeme)
            item_lex.setFont(mono_font)
            if token.is_error:
                item_lex.setForeground(QBrush(QColor("#fca5a5")))
                item_lex.setToolTip(f"Lexical error: {token.error_message}")
            self.token_table.setItem(row, 4, item_lex)

    def _filter_stream_table(self, text: str) -> None:
        """Filter the main token stream table dynamically as the user types."""
        search = text.strip().lower()
        visible_count = 0
        for row in range(self.token_table.rowCount()):
            if not search:
                self.token_table.setRowHidden(row, False)
                visible_count += 1
                continue

            matches = False
            for col in range(self.token_table.columnCount()):
                item = self.token_table.item(row, col)
                if item and search in item.text().lower():
                    matches = True
                    break

            self.token_table.setRowHidden(row, not matches)
            if matches:
                visible_count += 1

        self.table_count_label.setText(f"{visible_count} visible")

    def _populate_symbol_table(self, symbol_table: List[SymbolTableEntry]) -> None:
        """Populate the consolidated unique Symbol Table overview."""
        self.symbol_table_widget.setRowCount(0)
        self.symbol_table_widget.setRowCount(len(symbol_table))
        self.symbol_count_label.setText(f"{len(symbol_table)} unique entries")

        mono_font = QFont("Cascadia Code")
        mono_font.setStyleHint(QFont.Monospace)
        mono_font.setPointSize(10)

        badge_font = QFont()
        badge_font.setBold(True)
        badge_font.setPointSize(9)

        for row, entry in enumerate(symbol_table):
            # Column 0: Lexeme
            item_lex = QTableWidgetItem(entry.lexeme)
            item_lex.setFont(mono_font)
            self.symbol_table_widget.setItem(row, 0, item_lex)

            # Column 1: Category Badge
            item_cat = QTableWidgetItem(entry.category)
            item_cat.setTextAlignment(Qt.AlignCenter)
            bg, fg = get_token_type_badge_color(entry.token_type, entry.category)
            item_cat.setBackground(QBrush(QColor(bg)))
            item_cat.setForeground(QBrush(QColor(fg)))
            item_cat.setFont(badge_font)
            self.symbol_table_widget.setItem(row, 1, item_cat)

            # Column 2: Token Type
            item_type = QTableWidgetItem(entry.token_type)
            item_type.setTextAlignment(Qt.AlignCenter)
            self.symbol_table_widget.setItem(row, 2, item_type)

            # Column 3: Count
            item_count = QTableWidgetItem(str(entry.count))
            item_count.setTextAlignment(Qt.AlignCenter)
            self.symbol_table_widget.setItem(row, 3, item_count)

            # Column 4: Lines
            lines_str = ", ".join(str(l) for l in entry.lines)
            item_lines = QTableWidgetItem(lines_str)
            item_lines.setTextAlignment(Qt.AlignCenter)
            self.symbol_table_widget.setItem(row, 4, item_lines)

    def _populate_category_tables(self, tokens: List[Token]) -> None:
        """Populate the specific category viewer tabs (Keywords, Identifiers, Literals, Operators)."""
        categories = ["Keyword", "Identifier", "Literal", "Operator"]
        mono_font = QFont("Cascadia Code")
        mono_font.setStyleHint(QFont.Monospace)
        mono_font.setPointSize(10)

        badge_font = QFont()
        badge_font.setBold(True)
        badge_font.setPointSize(9)

        for cat in categories:
            cat_tokens = [t for t in tokens if t.category == cat]
            table: QTableWidget = getattr(self, f"table_{cat.lower()}")
            label: QLabel = getattr(self, f"label_{cat.lower()}")

            table.setRowCount(0)
            table.setRowCount(len(cat_tokens))
            label.setText(f"{len(cat_tokens)} {cat.lower()}(s)")

            for row, token in enumerate(cat_tokens):
                # #
                item_idx = QTableWidgetItem(str(token.index))
                item_idx.setTextAlignment(Qt.AlignCenter)
                table.setItem(row, 0, item_idx)

                # Line
                item_line = QTableWidgetItem(str(token.line_number))
                item_line.setTextAlignment(Qt.AlignCenter)
                table.setItem(row, 1, item_line)

                # Lexeme
                item_lex = QTableWidgetItem(token.lexeme)
                item_lex.setFont(mono_font)
                table.setItem(row, 2, item_lex)

                # Token Type Badge
                item_type = QTableWidgetItem(token.token_type)
                item_type.setTextAlignment(Qt.AlignCenter)
                bg, fg = get_token_type_badge_color(token.token_type, token.category)
                item_type.setBackground(QBrush(QColor(bg)))
                item_type.setForeground(QBrush(QColor(fg)))
                item_type.setFont(badge_font)
                table.setItem(row, 3, item_type)

    def _update_statistics_view(self, stats: TokenStatistics, line_count: int) -> None:
        """Update stat card labels with current counts."""
        self.stat_widgets["total_tokens"].setText(str(stats.total_tokens))
        self.stat_widgets["keywords"].setText(str(stats.keywords))
        self.stat_widgets["identifiers"].setText(str(stats.identifiers))
        self.stat_widgets["literals"].setText(str(stats.literals))
        self.stat_widgets["operators"].setText(str(stats.operators))
        self.stat_widgets["punctuators"].setText(str(stats.punctuators))
        self.stat_widgets["comments"].setText(str(stats.comments))
        self.stat_widgets["preprocessors"].setText(str(stats.preprocessors))

        errors_label = self.stat_widgets["errors"]
        errors_label.setText(str(stats.errors))
        if stats.errors > 0:
            errors_label.setStyleSheet(
                f"font-family: {FONT_FAMILY_MONO}; font-size: 18px; font-weight: 700; color: #f87171;"
            )
        else:
            errors_label.setStyleSheet(
                f"font-family: {FONT_FAMILY_MONO}; font-size: 18px; font-weight: 700; color: #38bdf8;"
            )

        self.summary_desc_label.setText(
            f"Analysis complete: Processed {line_count} source line(s) producing {stats.total_tokens} valid lexical tokens, "
            f"{stats.keywords} keywords, {stats.identifiers} identifiers, {stats.operators} operators, and {stats.errors} error(s)."
        )

    def _update_errors_view(self, errors: List[Token]) -> None:
        """Update the dedicated lexical errors tab with invalid characters."""
        # Clear existing error widgets in the frame
        while self.error_content_layout.count():
            item = self.error_content_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        self.error_table.setRowCount(0)
        self.error_table.setRowCount(len(errors))

        mono_font = QFont(FONT_FAMILY_MONO, 10)

        if not errors:
            self.error_content_frame.setProperty("class", "errorPanelNoErrors")
            self.error_content_frame.setStyleSheet(
                "background-color: #064e3b; border: 1px solid #059669; border-radius: 6px; padding: 8px 12px;"
            )
            lbl = QLabel("✓ No lexical errors detected — All characters recognized successfully")
            lbl.setStyleSheet("color: #34d399; font-weight: 600; font-size: 12px;")
            self.error_content_layout.addWidget(lbl)
        else:
            self.error_content_frame.setProperty("class", "errorPanelHasErrors")
            self.error_content_frame.setStyleSheet(
                "background-color: #450a0a; border: 1px solid #dc2626; border-radius: 6px; padding: 8px 12px;"
            )
            header_lbl = QLabel(f"⚠ Detected {len(errors)} lexical error(s) in source code:")
            header_lbl.setStyleSheet("color: #fca5a5; font-weight: 700; font-size: 12px;")
            self.error_content_layout.addWidget(header_lbl)

            for row, err in enumerate(errors):
                # Token #
                item_idx = QTableWidgetItem(str(err.index))
                item_idx.setTextAlignment(Qt.AlignCenter)
                self.error_table.setItem(row, 0, item_idx)

                # Line #
                item_line = QTableWidgetItem(str(err.line_number))
                item_line.setTextAlignment(Qt.AlignCenter)
                self.error_table.setItem(row, 1, item_line)

                # Lexeme
                item_lex = QTableWidgetItem(err.lexeme)
                item_lex.setFont(mono_font)
                item_lex.setForeground(QBrush(QColor("#fca5a5")))
                item_lex.setTextAlignment(Qt.AlignCenter)
                self.error_table.setItem(row, 2, item_lex)

                # Diagnostic
                item_diag = QTableWidgetItem(f"Invalid character or unrecognized symbol '{err.lexeme}'")
                item_diag.setForeground(QBrush(QColor("#fecaca")))
                self.error_table.setItem(row, 3, item_diag)

    def on_open_file(self) -> None:
        """Open a C source file (.c, .h, .txt) and load its content into the editor."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open C Source Code File",
            str(Path.cwd()),
            "C Source Files (*.c *.h *.txt);;All Files (*)",
        )
        if not file_path:
            return

        try:
            path_obj = Path(file_path)
            content = path_obj.read_text(encoding="utf-8")
            self.expression_editor.setPlainText(content)
            self.status_bar.showMessage(f"● Loaded file: {path_obj.name}")
            self.on_tokenize()
        except UnicodeDecodeError:
            try:
                content = Path(file_path).read_text(encoding="latin-1")
                self.expression_editor.setPlainText(content)
                self.status_bar.showMessage(f"● Loaded file: {Path(file_path).name}")
                self.on_tokenize()
            except Exception as exc:
                QMessageBox.critical(self, "Read Error", f"Unable to read file:\n{exc}")
        except Exception as exc:
            QMessageBox.critical(self, "Read Error", f"Unable to read file:\n{exc}")

    def on_save_results(self) -> None:
        """Export the complete analysis report to a text file."""
        input_text = self.expression_editor.toPlainText().strip()
        if not input_text and not self.current_tokens:
            QMessageBox.warning(
                self,
                "No Data to Save",
                "Please tokenize C source code before saving results.",
            )
            return

        default_name = "c_compiler_lexical_report.txt"
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Analysis Results",
            str(Path.cwd() / default_name),
            "Text Files (*.txt);;All Files (*)",
        )
        if not file_path:
            return

        try:
            report_text = format_save_report(
                input_text=input_text,
                tokens=self.current_tokens,
                stats=self.current_stats,
                errors=self.current_errors,
                symbol_table=self.current_symbol_table,
            )
            Path(file_path).write_text(report_text, encoding="utf-8")
            self.status_bar.showMessage(f"● Results saved to: {Path(file_path).name}")
            QMessageBox.information(
                self,
                "Save Successful",
                f"Compiler lexical analysis report successfully saved to:\n{file_path}",
            )
        except Exception as exc:
            QMessageBox.critical(
                self,
                "Save Error",
                f"Failed to save results:\n{exc}",
            )

    def on_clear(self) -> None:
        """Reset the code editor, tables, statistics, and error views."""
        self.expression_editor.clear()
        self.sample_combo.setCurrentIndex(0)
        self.token_table.setRowCount(0)
        self.table_count_label.setText("0 tokens")
        self.quick_stats_label.setText("0 tokens | 0 lines")

        self.current_tokens = []
        self.current_errors = []
        self.current_symbol_table = []
        self.current_stats = TokenStatistics()

        self._populate_symbol_table([])
        self._populate_category_tables([])
        self._update_statistics_view(self.current_stats, 0)
        self._update_errors_view([])
        self._check_engine_status()
        self.status_bar.showMessage("● Ready")
