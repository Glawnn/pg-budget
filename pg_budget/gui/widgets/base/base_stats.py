from PySide6.QtWidgets import QFrame, QGridLayout

from pg_budget.gui.widgets.stat_item import StatItem


class BaseStats(QFrame):
    """Base class for statistic display widgets"""

    def __init__(self, items: list[StatItem], columns=2, parent=None):
        """
        items: list of StatItem objects
        columns: number of columns in the grid
        """
        super().__init__(parent)
        self._layout = QGridLayout()
        self.setLayout(self._layout)
        self._stats = {}
        self.columns = columns

        if items:
            self._setup_items(items)

    def _setup_items(self, items: list[StatItem]):
        """Add StatItem widgets to the grid automatically"""
        for i, item in enumerate(items):
            row, col = divmod(i, self.columns)
            self._layout.addWidget(item, row, col)
            self._stats[item._id] = item

    def set_value(self, stat_id, value):
        """Update one stat by id"""
        if stat_id in self._stats:
            self._stats[stat_id].set_value(value)
        else:
            raise KeyError(f"No StatItem with id '{stat_id}' found.")

    def reset_values(self):
        """Reset all stats to '0'"""
        for stat in self._stats.values():
            stat.set_value("0")

    def update_stats(self, data):
        """Abstract method"""
        raise NotImplementedError
