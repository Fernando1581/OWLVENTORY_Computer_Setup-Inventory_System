import os
from PyQt6 import QtWidgets, QtGui
from views.ui_stockOutDialog import Ui_Dialog

class StockOutView(QtWidgets.QDialog):
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

    def bind_buttons(self, on_transfer, on_damaged):
        self.ui.transferedButton.clicked.connect(on_transfer)
        self.ui.checkButton_2.clicked.connect(on_damaged)

    def close_dialog(self):
        self.accept()