from datetime import datetime
from PySide6.QtWidgets import QWidget, QHBoxLayout, QComboBox, QPushButton
from PySide6.QtCore import Signal



class MonthYearPicker(QWidget):
    month_changed = Signal(int, int)

    def __init__(self):
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.now = datetime.now()

        # --- Bouton Moins (mois précédent) ---
        self.prev_button = QPushButton("◀")
        self.prev_button.setFixedWidth(30)
        self.prev_button.clicked.connect(self.prev_month)
        layout.addWidget(self.prev_button)


        # --- Combo mois ---
        self.month_selector = QComboBox()
        self.month_selector.addItems([
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ])
        self.month_selector.setCurrentIndex(self.now.month - 1)
        layout.addWidget(self.month_selector)


        # --- Combo année ---
        self.year_selector = QComboBox()
        years = [str(year) for year in range(self.now.year - 5, self.now.year + 6)]
        self.year_selector.addItems(years)
        self.year_selector.setCurrentText(str(self.now.year))
        layout.addWidget(self.year_selector)

        # --- Bouton Plus (mois suivant) ---
        self.next_button = QPushButton("▶")
        self.next_button.setFixedWidth(30)
        self.next_button.clicked.connect(self.next_month)
        layout.addWidget(self.next_button)

        # --- Bouton Aujourd'hui ---
        self.today_button = QPushButton("Today")
        self.today_button.setFixedWidth(60)
        self.today_button.clicked.connect(self.go_to_today)
        layout.addWidget(self.today_button)

        # Signaux
        self.month_selector.currentIndexChanged.connect(self._emit_signal)
        self.year_selector.currentIndexChanged.connect(self._emit_signal)

    def _emit_signal(self):
        year = int(self.year_selector.currentText())
        month = self.month_selector.currentIndex() + 1
        self.month_changed.emit(year, month)

    def get_year_month(self):
        year = int(self.year_selector.currentText())
        month = self.month_selector.currentIndex() + 1
        return year, month
    
    def set_year_month(self, year: int, month: int):
        year_index = self.year_selector.findText(str(year))
        if year_index != -1:
            self.year_selector.setCurrentIndex(year_index)
        
        month_index = month - 1
        if 0 <= month_index < self.month_selector.count():
            self.month_selector.setCurrentIndex(month_index)


    def prev_month(self):
        month = self.month_selector.currentIndex() + 1
        year = int(self.year_selector.currentText())
        month -= 1
        if month < 1:
            month = 12
            year -= 1
        self.set_year_month(year, month)

    def next_month(self):
        month = self.month_selector.currentIndex() + 1
        year = int(self.year_selector.currentText())
        month += 1
        if month > 12:
            month = 1
            year += 1
        self.set_year_month(year, month)

    def go_to_today(self):
        self.set_year_month(self.now.year, self.now.month)