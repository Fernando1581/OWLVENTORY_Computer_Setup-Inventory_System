import os
from PyQt6 import QtWidgets, QtGui
from views.ui_RequestForm import Ui_Dialog as UiRequest
from models.employee import EmployeeModel


class RequestController:
    def __init__(self, parent_view, emp_id, pc_no):
        self.dialog = QtWidgets.QDialog(parent_view)
        self.ui = UiRequest()
        self.ui.setupUi(self.dialog)

        self.emp_id = emp_id
        self.pc_no = pc_no

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.ui.label.setPixmap(QtGui.QPixmap(os.path.join(base_dir, "Images", "Untitled design (4).png")))

        self.ui.pushButton.clicked.connect(self.submit_request)

    def submit_request(self):
        hardware = self.ui.comboBox.currentText()
        reason = self.ui.plainTextEdit.toPlainText()

        if not reason.strip():
            QtWidgets.QMessageBox.warning(self.dialog, "Error", "Reason field cannot be empty.")
            return

        try:
            EmployeeModel.save_request(self.pc_no, self.emp_id, hardware, reason)
            QtWidgets.QMessageBox.information(self.dialog, "Success", "Request submitted to Admin.")
            self.dialog.accept()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self.dialog, "Error", f"Failed to submit: {e}")

    def show(self):
        self.dialog.exec()