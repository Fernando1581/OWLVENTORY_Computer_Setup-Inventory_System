import os
from PyQt6 import QtWidgets, QtGui, QtCore
from views.ui_itemsAdded import Ui_Dialog
from models.admin import AdminModel


class ItemsAddedController(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        img_folder = os.path.join(base_dir, "Images")
        img_path = os.path.join(img_folder, "Untitled design (4).png")

        if os.path.exists(img_path):
            self.ui.label.setPixmap(QtGui.QPixmap(img_path))

        self.ui.tableWidget.verticalHeader().setVisible(False)
        self.load_data()

    def load_data(self):
        try:
            logs = AdminModel.get_stock_logs()

            self.ui.tableWidget.setRowCount(0)

            for row_idx, row_data in enumerate(logs):
                self.ui.tableWidget.insertRow(row_idx)
                for col_idx, value in enumerate(row_data):
                    item = QtWidgets.QTableWidgetItem(str(value))
                    item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    self.ui.tableWidget.setItem(row_idx, col_idx, item)

        except Exception as e:
            print(f"Error loading items added history: {e}")