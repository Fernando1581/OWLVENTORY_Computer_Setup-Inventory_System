import os
from PyQt6 import QtWidgets, QtGui, QtCore
from views.ui_stockOutDialog import Ui_Dialog as UiStockOut
from views.ui_itemsAdded import Ui_Dialog as UiItemsAdded
from views.ui_ReportAction import Ui_Dialog as UiReportAction
from views.ui_ReportFix import Ui_Dialog as UiReportFix
from views.ui_HardwareChange import Ui_Dialog as UiHardwareChange
from views.ui_ReportForm import Ui_Dialog as UiReportForm


def _setup_img(label):
    try:
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        label.setPixmap(QtGui.QPixmap(os.path.join(base, "Images", "Untitled design (4).png")))
    except:
        pass


class StockOutView(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.ui = UiStockOut()
        self.ui.setupUi(self)
        _setup_img(self.ui.label)

    def bind(self, on_transfer, on_damaged):
        self.ui.transferedButton.clicked.connect(on_transfer)
        self.ui.checkButton_2.clicked.connect(on_damaged)


class ReportFormView(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.ui = UiReportForm()
        self.ui.setupUi(self)
        _setup_img(self.ui.label)

    def bind(self, on_submit):
        self.ui.pushButton.clicked.connect(on_submit)

    def get_text(self):
        return self.ui.plainTextEdit.toPlainText()

    def show_msg(self, msg, error=False):
        if error:
            QtWidgets.QMessageBox.critical(self, "Error", msg)
        else:
            QtWidgets.QMessageBox.information(self, "Info", msg)


class ItemsAddedView(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.ui = UiItemsAdded()
        self.ui.setupUi(self)
        _setup_img(self.ui.label)
        self.ui.tableWidget.verticalHeader().setVisible(False)
        self.ui.date1Filter.setCalendarPopup(True)
        self.ui.date2Filter.setCalendarPopup(True)
        self.ui.date1Filter.setDate(QtCore.QDate.currentDate())
        self.ui.date2Filter.setDate(QtCore.QDate.currentDate())

    def bind(self, on_combo, on_apply, on_gen):
        self.ui.reportFilterCB.currentIndexChanged.connect(on_combo)
        self.ui.applyButton.clicked.connect(on_apply)
        self.ui.generateReportButton.clicked.connect(on_gen)

    def set_dates(self, d1, d2):
        self.ui.date1Filter.setDate(d1)
        self.ui.date2Filter.setDate(d2)

    def get_dates(self):
        # Return Python date objects
        return self.ui.date1Filter.date().toPyDate(), self.ui.date2Filter.date().toPyDate()

    def get_combo_text(self):
        return self.ui.reportFilterCB.currentText()

    def update_table(self, data):
        self.ui.tableWidget.setRowCount(0)
        for r, row in enumerate(data):
            self.ui.tableWidget.insertRow(r)
            for c, val in enumerate(row):
                item = QtWidgets.QTableWidgetItem(str(val))
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.ui.tableWidget.setItem(r, c, item)

    def get_table_headers_and_data(self):
        rows = self.ui.tableWidget.rowCount()
        cols = self.ui.tableWidget.columnCount()
        headers = [self.ui.tableWidget.horizontalHeaderItem(c).text() for c in range(cols)]
        data = []
        for r in range(rows):
            row_d = []
            for c in range(cols):
                it = self.ui.tableWidget.item(r, c)
                row_d.append(it.text() if it else "")
            data.append(row_d)
        return headers, data

    def open_save_dialog(self, name):
        path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save", name, "PDF (*.pdf)")
        return path

    def show_msg(self, msg):
        QtWidgets.QMessageBox.information(self, "Info", msg)


# --- The 3-Step Request Action Dialogs ---
class ActionView(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.ui = UiReportAction()
        self.ui.setupUi(self)
        _setup_img(self.ui.label)

    def set_info(self, pc, name, reason):
        self.ui.pcNo.setText(str(pc))
        self.ui.reqName.setText(str(name))
        self.ui.reason.setText(str(reason))

    def bind(self, on_ignore, on_check):
        self.ui.ignoreButton.clicked.connect(on_ignore)
        self.ui.checkButton.clicked.connect(on_check)

    def show_msg(self, msg): QtWidgets.QMessageBox.information(self, "Info", msg)


class FixView(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.ui = UiReportFix()
        self.ui.setupUi(self)
        _setup_img(self.ui.label)

    def bind(self, on_normal, on_hw):
        self.ui.checkButton.clicked.connect(on_normal)
        self.ui.checkButton_2.clicked.connect(on_hw)


class HWView(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.ui = UiHardwareChange()
        self.ui.setupUi(self)
        _setup_img(self.ui.label)

    def bind(self, on_grant):
        self.ui.grantBtn.clicked.connect(on_grant)

    def get_selection(self):
        return self.ui.hardwareComboBox.currentText(), self.ui.technicianComboBox.currentText()

    def show_msg(self, msg, error=False):
        if error:
            QtWidgets.QMessageBox.warning(self, "Warning", msg)
        else:
            QtWidgets.QMessageBox.information(self, "Info", msg)