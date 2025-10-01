from PySide6.QtWidgets import QCheckBox
import pytest


def present_in_table(table, expected):
    for row in table.rows:
        match = True
        for col, val in expected.items():
            widget = row.get_widget_by_name(col)

            if isinstance(widget, QCheckBox):
                widget_val = widget.isChecked()
            else:
                widget_val = widget.text()

            if widget_val != val:
                match = False
                break
        if match:
            return True

    # If we reach here -> no row matched, dump table content
    all_rows = []
    for i, row in enumerate(table.rows):
        row_repr = {}
        for col in expected.keys():
            widget = row.get_widget_by_name(col)
            if isinstance(widget, QCheckBox):
                row_repr[col] = widget.isChecked()
            else:
                row_repr[col] = widget.text()
        all_rows.append(f"Row {i}: {row_repr}")

    pytest.fail(f"No row matches {expected}\nTable content:\n" + "\n".join(all_rows))


def absent_in_table(table, expected):
    for row in table.rows:
        match = True
        for col, val in expected.items():
            widget = row.get_widget_by_name(col)
            widget_val = widget.isChecked() if isinstance(widget, QCheckBox) else widget.text()
            if widget_val != val:
                match = False
                break
        if match:
            pytest.fail(f"Unexpected row found: {expected}")
    return True


def get_row_in_table(table, expected):
    for row in table.rows:
        if all(row.get_widget_by_name(col).text() == val for col, val in expected.items()):
            return row
    return None
