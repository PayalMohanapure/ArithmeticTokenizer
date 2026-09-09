"""Application Entry Point for Arithmetic Expression Tokenizer UI.

Initializes PySide6 application, configures high-DPI attributes,
and presents the main window.
"""

import sys
from pathlib import Path

# Ensure project root is in sys.path when launched directly
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow


def main() -> None:
    """Launch the Arithmetic Expression Tokenizer Desktop Application."""
    app = QApplication(sys.argv)
    app.setApplicationName("Arithmetic Expression Tokenizer")
    app.setOrganizationName("CompilerDesignProject")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
