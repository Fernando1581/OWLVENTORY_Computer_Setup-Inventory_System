import os
from PyQt6 import QtWidgets, QtGui, QtCore
from views.ui_itemsAdded import Ui_Dialog


class ItemsAddedView(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.tableWidget.verticalHeader().setVisible(False)
        self.setup_images()

        # Setup Date Pickers
        self.ui.date1Filter.setCalendarPopup(True)
        self.ui.date2Filter.setCalendarPopup(True)
        self.ui.date1Filter.setDate(QtCore.QDate.currentDate())
        self.ui.date2Filter.setDate(QtCore.QDate.currentDate())

    def setup_images(self):
        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            img_path = os.path.join(base_dir, "Images", "Untitled design (4).png")
            self.ui.label.setPixmap(QtGui.QPixmap(img_path))
        except Exception:
            pass

    # --- Bindings ---
    def bind_filter_change(self, callback):
        self.ui.reportFilterCB.currentIndexChanged.connect(callback)

    def bind_apply(self, callback):
        self.ui.applyButton.clicked.connect(callback)

    def bind_generate(self, callback):
        self.ui.generateReportButton.clicked.connect(callback)

    # --- Getters/Setters ---
    def get_filter_mode(self):
        return self.ui.reportFilterCB.currentText()

    def set_date_range(self, start_date, end_date):
        # Accepts Python date objects, converts to QDate
        self.ui.date1Filter.setDate(start_date)
        self.ui.date2Filter.setDate(end_date)

    def get_date_range(self):
        # Returns Python date objects
        return self.ui.date1Filter.date().toPyDate(), self.ui.date2Filter.date().toPyDate()

    def update_table(self, data):
        self.ui.tableWidget.setRowCount(0)
        if not data: return

        for r, row in enumerate(data):
            self.ui.tableWidget.insertRow(r)
            for c, val in enumerate(row):
                item = QtWidgets.QTableWidgetItem(str(val))
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.ui.tableWidget.setItem(r, c, item)

    def get_table_data_for_pdf(self):
        rows = self.ui.tableWidget.rowCount()
        cols = self.ui.tableWidget.columnCount()
        headers = [self.ui.tableWidget.horizontalHeaderItem(c).text() for c in range(cols)]

        data_matrix = []
        for r in range(rows):
            row_data = []
            for c in range(cols):
                item = self.ui.tableWidget.item(r, c)
                row_data.append(item.text() if item else "")
            data_matrix.append(row_data)
        return headers, data_matrix

    def open_save_dialog(self, default_filename):
        path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Save Report", default_filename, "PDF (*.pdf)"
        )
        return path

    def show_message(self, title, msg, is_error=False):
        if is_error:
            QtWidgets.QMessageBox.critical(self, title, msg)
        else:
            QtWidgets.QMessageBox.information(self, title, msg)