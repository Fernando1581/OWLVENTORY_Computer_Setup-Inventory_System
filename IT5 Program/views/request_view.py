import os
from PyQt6 import QtWidgets, QtGui
from views.ui_ReportForm import Ui_Dialog

class RequestView(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setup_images()

    def setup_images(self):
        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            img_path = os.path.join(base_dir, "Images", "Untitled design (4).png")
            self.ui.label.setPixmap(QtGui.QPixmap(img_path))
        except Exception:
            pass

    def bind_submit(self, callback):
        self.ui.pushButton.clicked.connect(callback)

    def get_reason(self):
        return self.ui.plainTextEdit.toPlainText()

    def show_error(self, message):
        QtWidgets.QMessageBox.warning(self, "Error", message)

    def show_success(self, message):
        QtWidgets.QMessageBox.information(self, "Success", message)

    def close_dialog(self):
        self.accept()