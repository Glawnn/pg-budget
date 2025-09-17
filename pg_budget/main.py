import sys
from PySide6.QtWidgets import QApplication

from pg_budget.gui.windows import MainWindow


def main():
     app = QApplication(sys.argv)

     # Charger le style
     #with open("pg_budget/gui/styles/main_style.qss", "r") as f:
      #  app.setStyleSheet(f.read())

     window = MainWindow()
     window.show()
     sys.exit(app.exec())

if __name__ == "__main__":
    main()
