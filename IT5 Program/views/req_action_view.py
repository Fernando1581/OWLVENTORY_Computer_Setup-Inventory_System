import os
from PyQt6 import QtWidgets, QtGui
from views.ui_ReportAction import Ui_Dialog as UiReportAction
from views.ui_ReportFix import Ui_Dialog as UiReportFix
from views.ui_HardwareChange import Ui_Dialog as UiHardwareChange

def _setup_img(label):
    try:
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path = os.path.join(base, "Images", "Untitled design (4).png")
        label.setPixmap(QtGui.QPixmap(path))
    except: pass

class ActionView(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = UiReportAction()
        self.ui.setupUi(self)
        _setup_img(self.ui.label)

    def set_details(self, pc, name, reason):
        self.ui.pcNo.setText(str(pc))
        self.ui.reqName.setText(str(name))
        self.ui.reason.setText(str(reason))

    def bind_buttons(self, on_ignore, on_check):
        self.ui.ignoreButton.clicked.connect(on_ignore)
        self.ui.checkButton.clicked.connect(on_check)

    def show_message(self, msg, is_error=False):
        if is_error: QtWidgets.QMessageBox.critical(self, "Error", msg)
        else: QtWidgets.QMessageBox.information(self, "Info", msg)

class FixView(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = UiReportFix()
        self.ui.setupUi(self)
        _setup_img(self.ui.label)

    def bind_buttons(self, on_normal, on_hardware):
        self.ui.checkButton.clicked.connect(on_normal)
        self.ui.checkButton_2.clicked.connect(on_hardware)

    def show_error(self, msg):
        QtWidgets.QMessageBox.critical(self, "Error", msg)

    def show_success(self, msg):
        QtWidgets.QMessageBox.information(self, "Success", msg)

class HardwareView(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = UiHardwareChange()
        self.ui.setupUi(self)
        _setup_img(self.ui.label)

    def bind_grant(self, callback):
        self.ui.grantBtn.clicked.connect(callback)

    def get_selection(self):
        return self.ui.hardwareComboBox.currentText(), self.ui.technicianComboBox.currentText()

    def show_message(self, msg, is_error=False):
        if is_error: QtWidgets.QMessageBox.warning(self, "Failed", msg)
        else: QtWidgets.QMessageBox.information(self, "Success", msg)