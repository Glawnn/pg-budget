"""Entry point"""

import sys
from PySide6.QtWidgets import QApplication

from pg_budget.gui.windows import MainWindow


def main():
    """main entry point"""
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
