"""Main window"""

import os
from PySide6.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QStackedWidget,
    QFileDialog,
    QMessageBox,
    QMenu,
)
from PySide6.QtGui import QAction
from importlib.metadata import version


from pg_budget.core.db import db
from pg_budget.gui.views import ExpensesView, ExpensesPlanView
from pg_budget.gui.widgets.expense_plan_table import ExpensesPlanDialog
from pg_budget.gui.widgets.expenses_table import ExpenseDialog
from pg_budget.utils import resource_path


__version__ = "v" + version("pg-budget")


class MainWindow(QMainWindow):
    """Main window class"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"PG-Budget {__version__}")
        self.resize(800, 400)

        self._init()

    def _init(self):
        with open(resource_path("pg_budget/gui/styles/light_style.qss"), "r", encoding="utf-8") as file:
            qss = file.read()
            self.setStyleSheet(qss)

        self.menu = AppMenu(self)
        self.menu.init_menu_bar()

        self._create_central_widget()
        self._create_status_bar()

    def _create_central_widget(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        self.stacked_widget = QStackedWidget()
        layout.addWidget(self.stacked_widget)

        # --- Vue 1 : Expenses ---
        self.expenses_view = ExpensesView()
        self.stacked_widget.addWidget(self.expenses_view)

        # --- Vue 2 : Expenses Plan ---
        self.expenses_plan_view = ExpensesPlanView()
        self.stacked_widget.addWidget(self.expenses_plan_view)

    def _create_status_bar(self):
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Ready")


class AppMenu:
    """class for manage menu"""

    def __init__(self, main_window: MainWindow):
        self.main_window = main_window

    def init_menu_bar(self):
        """init the menubar"""
        self._init_file_menu()
        self._init_edit_menu()
        self._init_view_menu()

    def _init_file_menu(self):
        file_menu: QMenu = self.main_window.menuBar().addMenu("File")

        new_db_action = QAction("New User", self.main_window)
        new_db_action.triggered.connect(lambda: self.select_database(create=True))
        file_menu.addAction(new_db_action)

        open_db_action = QAction("Open User", self.main_window)
        open_db_action.triggered.connect(lambda: self.select_database(create=False))
        file_menu.addAction(open_db_action)

        exit_action = QAction("Exit", self.main_window)
        exit_action.triggered.connect(self.main_window.close)
        file_menu.addAction(exit_action)

    def select_database(self, create: bool = False):
        """select the db"""
        if create:
            file_path, _ = QFileDialog.getSaveFileName(
                self.main_window,
                "Create New Database",
                os.getcwd(),
                "JSON Files (*.json);;All Files (*)",
            )
        else:
            file_path, _ = QFileDialog.getOpenFileName(
                self.main_window,
                "Open Database",
                os.getcwd(),
                "JSON Files (*.json);;All Files (*)",
            )

        if not file_path:
            return  # annulé

        # Change la DB active
        db.set_path(file_path)

        msg = "New database created" if create else "Database loaded"
        QMessageBox.information(self.main_window, "Database", f"{msg}:\n{file_path}")

        # Affiche le chemin dans la status bar
        self.main_window.status_bar.showMessage(f"DB: {file_path}")

        self.main_window.expenses_view.load()
        self.main_window.expenses_plan_view.load()

    def _init_edit_menu(self):
        actions_menu: QMenu = self.main_window.menuBar().addMenu("Actions")

        add_expense = QAction("Add Expense", self.main_window)
        add_expense.triggered.connect(self.create_expense)
        actions_menu.addAction(add_expense)

        add_expense_plan = QAction("Add Expenses Plan", self.main_window)
        add_expense_plan.triggered.connect(self.create_expenses_plan)
        actions_menu.addAction(add_expense_plan)

        add_input = QAction("Add Input", self.main_window)
        add_input.triggered.connect(lambda: print("add input -> to be implemented"))
        actions_menu.addAction(add_input)

    def create_expense(self):
        """create an expense"""
        self.main_window.stacked_widget.setCurrentWidget(self.main_window.expenses_view)
        dialog = ExpenseDialog(parent=self.main_window)
        dialog.exec()
        self.main_window.expenses_view.load()
        self.main_window.expenses_view.load()

    def create_expenses_plan(self):
        """create expense plan"""
        self.main_window.stacked_widget.setCurrentWidget(self.main_window.expenses_plan_view)
        dialog = ExpensesPlanDialog(parent=self.main_window)
        dialog.exec()
        self.main_window.expenses_plan_view.load()

    def _init_view_menu(self):
        view_menu: QMenu = self.main_window.menuBar().addMenu("Views")

        show_expenses = QAction("Expenses View", self.main_window)
        show_expenses.triggered.connect(
            lambda: self.main_window.stacked_widget.setCurrentWidget(self.main_window.expenses_view)
        )
        view_menu.addAction(show_expenses)

        show_other = QAction("ExpensesPlan View", self.main_window)
        show_other.triggered.connect(
            lambda: self.main_window.stacked_widget.setCurrentWidget(self.main_window.expenses_plan_view)
        )
        view_menu.addAction(show_other)
