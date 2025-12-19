from PyQt6 import QtWidgets
from views.ui_reqAction import Ui_Dialog as UiReqAction
from models.admin import AdminModel


class ReqActionController:
    def __init__(self, parent_view, data, admin_id):
        self.dialog = QtWidgets.QDialog(parent_view)
        self.ui = UiReqAction()
        self.ui.setupUi(self.dialog)

        self.request_id = data[5]
        self.admin_id = admin_id  # Store the ID (e.g., 1 or 101)

        self.ui.employeeName.setText(str(data[2]))
        self.ui.hardware.setText(str(data[3]))
        self.ui.reason.setText(str(data[4]))

        self.ui.grantButton.clicked.connect(lambda: self.process("Granted"))
        self.ui.denyButton.clicked.connect(lambda: self.process("Denied"))

    def process(self, status):
        try:
            AdminModel.update_request_status(self.request_id, status, self.admin_id)
            self.dialog.accept()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self.dialog, "Error", str(e))

    def exec(self):
        return self.dialog.exec()