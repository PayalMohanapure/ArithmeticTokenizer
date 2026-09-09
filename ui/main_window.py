"""Main Window for Arithmetic Expression Tokenizer Desktop UI.

Implements the complete, modern, academic-tool GUI using PySide6.
"""

from pathlib import Path
from typing import List, Optional

from PySide6.QtCore import Qt, QSize
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
    QSizePolicy,
)

from ui.lexer_runner import run_lexer, find_lexer_executable
from ui.token_parser import parse_lexer_output, Token
from ui.statistics import (
    calculate_statistics,
    format_save_report,
    TokenStatistics,
)
from ui.styles import (
    GLOBAL_STYLESHEET,
    FONT_FAMILY_MONO,
    FONT_FAMILY_UI,
    get_token_type_badge_color,
)


SAMPLE_EXPRESSIONS = [
    ("Select a sample expression...", ""),
    ("Basic: 10 + 20 * 5", "10 + 20 * 5"),
    ("Variables: x = a + b * c", "x = a + b * c"),
    ("Floating Point: result = 12.5 + 3.14 * 2", "result = 12.5 + 3.14 * 2"),
    ("Parentheses: x = (a + b) * (c - d)", "x = (a + b) * (c - d)"),
    ("Invalid Input: x = 10 @ 20", "x = 10 @ 20"),
    ("Advanced Arithmetic: result = 12.5 + 3.14 * (x - 2)", "result = 12.5 + 3.14 * (x - 2)"),
    ("Power & Modulo: a = b ^ 2 % 5", "a = b ^ 2 % 5"),
    ("Multi-Identifier: total = price * quantity + tax", "total = price * quantity + tax"),
]


class MainWindow(QMainWindow):
    """Main Application Window for Arithmetic Expression Tokenizer."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Arithmetic Expression Tokenizer — Lexical Analysis using FLEX")
        self.resize(1080, 780)
        self.setMinimumSize(850, 600)

        # State
        self.current_tokens: List[Token] = []
        self.current_errors: List[Token] = []
        self.current_stats: TokenStatistics = TokenStatistics()

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
        main_layout.setContentsMargins(20, 16, 20, 12)
        main_layout.setSpacing(14)

        # 1. Header Section
        header_widget = self._create_header()
        main_layout.addWidget(header_widget)

        # 2. Expression Input & Controls Card
        input_card = self._create_input_card()
        main_layout.addWidget(input_card)

        # 3. Main Workspace Splitter (Token Table on Left, Stats & Errors on Right)
        workspace_splitter = QSplitter(Qt.Horizontal)
        workspace_splitter.setChildrenCollapsible(False)

        # Left Panel: Token Analysis Table
        table_panel = self._create_table_panel()
        workspace_splitter.addWidget(table_panel)

        # Right Panel: Statistics, Lexical Errors & Token Legend
        side_panel = self._create_side_panel()
        workspace_splitter.addWidget(side_panel)

        # Set balanced splitter proportions (58% table, 42% info panel)
        workspace_splitter.setStretchFactor(0, 58)
        workspace_splitter.setStretchFactor(1, 42)

        main_layout.addWidget(workspace_splitter, stretch=1)

        # 4. Status Bar
        self.status_bar = QStatusBar(self)
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("● Ready")

    def _create_header(self) -> QWidget:
        """Create the top title and engine status bar."""
        header = QFrame()
        layout = QHBoxLayout(header)
        layout.setContentsMargins(0, 0, 0, 0)

        title_box = QVBoxLayout()
        title_box.setSpacing(2)

        title_label = QLabel("ARITHMETIC TOKENIZER")
        title_label.setStyleSheet("font-size: 18px; font-weight: 800; color: #f8fafc; letter-spacing: 1px;")
        subtitle_label = QLabel("Lexical Analysis using FLEX")
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
        """Create the expression editor and control actions panel."""
        card = QFrame()
        card.setProperty("class", "cardPanel")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(14, 12, 14, 12)
        card_layout.setSpacing(10)

        # Top row: Label & Sample Selector
        top_row = QHBoxLayout()
        input_label = QLabel("ARITHMETIC EXPRESSION")
        input_label.setProperty("class", "sectionHeader")
        top_row.addWidget(input_label)

        top_row.addStretch()

        sample_label = QLabel("Sample:")
        sample_label.setStyleSheet("color: #94a3b8; font-size: 12px; font-weight: 500;")
        top_row.addWidget(sample_label)

        self.sample_combo = QComboBox()
        for label, _ in SAMPLE_EXPRESSIONS:
            self.sample_combo.addItem(label)
        self.sample_combo.currentIndexChanged.connect(self._on_sample_selected)
        top_row.addWidget(self.sample_combo)

        card_layout.addLayout(top_row)

        # Multiline Expression Editor
        self.expression_editor = QPlainTextEdit()
        self.expression_editor.setObjectName("expressionEditor")
        self.expression_editor.setPlaceholderText("Enter an arithmetic expression... (e.g., x = 25 + 3.14 * (y - 10))")
        self.expression_editor.setFixedHeight(85)
        card_layout.addWidget(self.expression_editor)

        # Action Buttons Row
        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)

        self.tokenize_btn = QPushButton("Tokenize")
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
        card_layout.addLayout(btn_row)

        return card

    def _create_table_panel(self) -> QFrame:
        """Create the structured token table view."""
        panel = QFrame()
        panel.setProperty("class", "cardPanel")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(10)

        header_layout = QHBoxLayout()
        table_title = QLabel("TOKEN ANALYSIS")
        table_title.setProperty("class", "sectionHeader")
        header_layout.addWidget(table_title)

        self.table_count_label = QLabel("0 tokens")
        self.table_count_label.setStyleSheet("color: #94a3b8; font-size: 12px; font-weight: 500;")
        header_layout.addStretch()
        header_layout.addWidget(self.table_count_label)
        layout.addLayout(header_layout)

        # Table Widget
        self.token_table = QTableWidget(0, 3)
        self.token_table.setObjectName("tokenTable")
        self.token_table.setHorizontalHeaderLabels(["#", "Lexeme", "Token Type"])
        self.token_table.verticalHeader().setVisible(False)
        self.token_table.setAlternatingRowColors(True)
        self.token_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.token_table.setEditTriggers(QTableWidget.NoEditTriggers)

        # Resize modes
        header = self.token_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)

        layout.addWidget(self.token_table)
        return panel

    def _create_side_panel(self) -> QWidget:
        """Create the right side panel containing Statistics, Errors, and Legend."""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        # 1. Statistics Panel
        stats_card = self._create_statistics_card()
        layout.addWidget(stats_card)

        # 2. Lexical Errors Panel
        errors_card = self._create_errors_card()
        layout.addWidget(errors_card)

        # 3. Token Information / Legend Panel
        legend_card = self._create_legend_card()
        layout.addWidget(legend_card, stretch=1)

        return container

    def _create_statistics_card(self) -> QFrame:
        """Create the categorized statistics display card."""
        card = QFrame()
        card.setProperty("class", "cardPanel")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(10)

        title = QLabel("STATISTICS")
        title.setProperty("class", "sectionHeader")
        layout.addWidget(title)

        grid = QGridLayout()
        grid.setSpacing(8)

        # Stat cards
        self.stat_widgets = {}
        metrics = [
            ("total_tokens", "Total Tokens", "0", 0, 0),
            ("identifiers", "Identifiers", "0", 0, 1),
            ("numbers", "Numbers", "0", 0, 2),
            ("operators", "Operators", "0", 1, 0),
            ("parentheses", "Parentheses", "0", 1, 1),
            ("errors", "Errors", "0", 1, 2),
        ]

        for key, label_text, default_val, row, col in metrics:
            stat_frame = QFrame()
            stat_frame.setProperty("class", "statCard")
            stat_layout = QVBoxLayout(stat_frame)
            stat_layout.setContentsMargins(8, 6, 8, 6)
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
        return card

    def _create_errors_card(self) -> QFrame:
        """Create the dedicated lexical errors display panel."""
        self.errors_card = QFrame()
        self.errors_card.setProperty("class", "cardPanel")
        layout = QVBoxLayout(self.errors_card)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(8)

        title = QLabel("LEXICAL ERRORS")
        title.setProperty("class", "sectionHeader")
        layout.addWidget(title)

        self.error_content_frame = QFrame()
        self.error_content_frame.setProperty("class", "errorPanelNoErrors")
        self.error_content_layout = QVBoxLayout(self.error_content_frame)
        self.error_content_layout.setContentsMargins(10, 8, 10, 8)

        self.error_status_label = QLabel("✓ No lexical errors detected")
        self.error_status_label.setStyleSheet("color: #34d399; font-weight: 600; font-size: 12px;")
        self.error_content_layout.addWidget(self.error_status_label)

        layout.addWidget(self.error_content_frame)
        return self.errors_card

    def _create_legend_card(self) -> QFrame:
        """Create the token information reference card."""
        card = QFrame()
        card.setProperty("class", "cardPanel")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(8)

        title = QLabel("TOKEN REFERENCE")
        title.setProperty("class", "sectionHeader")
        layout.addWidget(title)

        desc = QLabel("Supported token rules from FLEX lexer:")
        desc.setProperty("class", "subHeader")
        layout.addWidget(desc)

        legend_grid = QGridLayout()
        legend_grid.setSpacing(6)

        token_defs = [
            ("IDENTIFIER", "x, total, a1", "Identifiers [a-zA-Z_][a-zA-Z0-9_]*"),
            ("INTEGER", "10, 25, 100", "Whole number digits [0-9]+"),
            ("FLOAT", "3.14, 0.5", "Decimal digits [0-9]+\\.[0-9]+"),
            ("PLUS / MINUS", "+ , -", "Addition & Subtraction"),
            ("MULTIPLY / DIV", "* , /", "Multiplication & Division"),
            ("POWER / MOD", "^ , %", "Exponentiation & Modulo"),
            ("PARENTHESES", "( , )", "Grouping LPAREN & RPAREN"),
            ("ASSIGN", "=", "Assignment operator"),
        ]

        for i, (name, sym, desc_text) in enumerate(token_defs):
            row = i // 2
            col = (i % 2) * 2

            tag_lbl = QLabel(name)
            tag_lbl.setStyleSheet(
                "background-color: #1f2937; color: #38bdf8; font-family: "
                f"{FONT_FAMILY_MONO}; font-size: 11px; font-weight: 700; "
                "padding: 2px 6px; border-radius: 4px;"
            )
            legend_grid.addWidget(tag_lbl, row, col)

            detail_lbl = QLabel(desc_text)
            detail_lbl.setStyleSheet("color: #94a3b8; font-size: 11px;")
            legend_grid.addWidget(detail_lbl, row, col + 1)

        layout.addLayout(legend_grid)
        layout.addStretch()
        return card

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
        """Load a selected sample expression into the input editor."""
        if 0 < index < len(SAMPLE_EXPRESSIONS):
            _, expression = SAMPLE_EXPRESSIONS[index]
            self.expression_editor.setPlainText(expression)
            self.status_bar.showMessage(f"● Loaded sample expression: {SAMPLE_EXPRESSIONS[index][0]}")

    def on_tokenize(self) -> None:
        """Run the existing FLEX lexer on the input expression and display results."""
        expression = self.expression_editor.toPlainText().strip()
        if not expression:
            QMessageBox.warning(
                self,
                "Empty Expression",
                "Please enter an arithmetic expression.",
            )
            self.expression_editor.setFocus()
            return

        self._check_engine_status()

        # Run authoritative lexer binary
        result = run_lexer(expression)
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

        # Calculate statistics
        self.current_stats = calculate_statistics(parsed.tokens, parsed.errors)

        # Update UI views
        self._populate_table(parsed.tokens)
        self._update_statistics_view(self.current_stats)
        self._update_errors_view(parsed.errors)

        if parsed.error_count == 0:
            self.status_bar.showMessage(
                f"● Tokenization completed: {self.current_stats.total_tokens} tokens recognized"
            )
        else:
            self.status_bar.showMessage(
                f"● Tokenization completed with {parsed.error_count} lexical error(s)"
            )

    def _populate_table(self, tokens: List[Token]) -> None:
        """Fill the token table widget with parsed tokens."""
        self.token_table.setRowCount(0)
        self.token_table.setRowCount(len(tokens))
        self.table_count_label.setText(f"{len(tokens)} token(s)")

        mono_font = QFont()
        mono_font.setFamily("Cascadia Code")
        mono_font.setPointSize(10)

        for row, token in enumerate(tokens):
            # Column 0: Token Index (#)
            item_idx = QTableWidgetItem(str(token.index))
            item_idx.setTextAlignment(Qt.AlignCenter)
            self.token_table.setItem(row, 0, item_idx)

            # Column 1: Lexeme
            item_lex = QTableWidgetItem(token.lexeme)
            item_lex.setFont(mono_font)
            if token.is_error:
                item_lex.setForeground(QBrush(QColor("#fca5a5")))
            self.token_table.setItem(row, 1, item_lex)

            # Column 2: Token Type
            item_type = QTableWidgetItem(token.token_type)
            item_type.setTextAlignment(Qt.AlignCenter)

            bg_color, fg_color = get_token_type_badge_color(token.token_type)
            item_type.setBackground(QBrush(QColor(bg_color)))
            item_type.setForeground(QBrush(QColor(fg_color)))

            font = item_type.font()
            font.setBold(True)
            item_type.setFont(font)

            if token.is_error:
                item_type.setToolTip(f"Lexical error: {token.error_message}")

            self.token_table.setItem(row, 2, item_type)

    def _update_statistics_view(self, stats: TokenStatistics) -> None:
        """Update stat card labels with current counts."""
        self.stat_widgets["total_tokens"].setText(str(stats.total_tokens))
        self.stat_widgets["identifiers"].setText(str(stats.identifiers))
        self.stat_widgets["numbers"].setText(str(stats.numbers))
        self.stat_widgets["operators"].setText(str(stats.operators))
        self.stat_widgets["parentheses"].setText(str(stats.parentheses))

        errors_label = self.stat_widgets["errors"]
        errors_label.setText(str(stats.errors))
        if stats.errors > 0:
            errors_label.setStyleSheet(
                f"font-family: {FONT_FAMILY_MONO}; font-size: 20px; font-weight: 700; color: #f87171;"
            )
        else:
            errors_label.setStyleSheet(
                f"font-family: {FONT_FAMILY_MONO}; font-size: 20px; font-weight: 700; color: #38bdf8;"
            )

    def _update_errors_view(self, errors: List[Token]) -> None:
        """Update the lexical error panel with detected invalid characters."""
        # Clear existing error widgets
        while self.error_content_layout.count():
            item = self.error_content_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        if not errors:
            self.error_content_frame.setStyleSheet(
                "background-color: #064e3b; border: 1px solid #059669; border-radius: 6px; padding: 8px 12px;"
            )
            lbl = QLabel("✓ No lexical errors detected")
            lbl.setStyleSheet("color: #34d399; font-weight: 600; font-size: 12px;")
            self.error_content_layout.addWidget(lbl)
        else:
            self.error_content_frame.setStyleSheet(
                "background-color: #450a0a; border: 1px solid #dc2626; border-radius: 6px; padding: 8px 12px;"
            )
            header_lbl = QLabel(f"⚠ Detected {len(errors)} lexical error(s):")
            header_lbl.setStyleSheet("color: #fca5a5; font-weight: 700; font-size: 12px;")
            self.error_content_layout.addWidget(header_lbl)

            for err in errors:
                err_text = f"•  {err.lexeme}   →   Invalid character (Token #{err.index})"
                err_lbl = QLabel(err_text)
                err_lbl.setStyleSheet(
                    f"color: #fecaca; font-family: {FONT_FAMILY_MONO}; font-size: 12px; font-weight: 600;"
                )
                self.error_content_layout.addWidget(err_lbl)

    def on_open_file(self) -> None:
        """Open a text file and load its content into the expression editor."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Expression File",
            str(Path.cwd()),
            "Text Files (*.txt);;All Files (*)",
        )
        if not file_path:
            return

        try:
            path_obj = Path(file_path)
            content = path_obj.read_text(encoding="utf-8")
            self.expression_editor.setPlainText(content)
            self.status_bar.showMessage(f"● Loaded file: {path_obj.name}")
        except UnicodeDecodeError:
            try:
                content = Path(file_path).read_text(encoding="latin-1")
                self.expression_editor.setPlainText(content)
                self.status_bar.showMessage(f"● Loaded file: {Path(file_path).name}")
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
                "Please tokenize an expression before saving results.",
            )
            return

        default_name = "tokenization_results.txt"
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
            )
            Path(file_path).write_text(report_text, encoding="utf-8")
            self.status_bar.showMessage(f"● Results saved to: {Path(file_path).name}")
            QMessageBox.information(
                self,
                "Save Successful",
                f"Analysis report successfully saved to:\n{file_path}",
            )
        except Exception as exc:
            QMessageBox.critical(
                self,
                "Save Error",
                f"Failed to save results:\n{exc}",
            )

    def on_clear(self) -> None:
        """Reset the expression editor, table, statistics, and error views."""
        self.expression_editor.clear()
        self.sample_combo.setCurrentIndex(0)
        self.token_table.setRowCount(0)
        self.table_count_label.setText("0 tokens")

        self.current_tokens = []
        self.current_errors = []
        self.current_stats = TokenStatistics()

        self._update_statistics_view(self.current_stats)
        self._update_errors_view([])
        self._check_engine_status()
        self.status_bar.showMessage("● Ready")
