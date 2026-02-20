import os
from datetime import datetime
from PyQt6 import QtWidgets, QtGui, QtCore
from views.ui_Admin import Ui_MainWindow

try:
    from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
    from matplotlib.figure import Figure
    import matplotlib.pyplot as plt

    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False


class AdminView(QtWidgets.QMainWindow):
    def __init__(self, admin_name):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup_ui_extras(admin_name)
        self.setup_tables()
        self.init_graph()

        self._setup_callbacks = {}

    def setup_ui_extras(self, name):
        self.ui.label_3.setText(f"Manager: {name}")
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        img_folder = os.path.join(base_dir, "Images")
        try:
            self.ui.label.setPixmap(QtGui.QPixmap(os.path.join(img_folder, "Untitled design (2).png")))
            self.ui.personIcon.setPixmap(QtGui.QPixmap(os.path.join(img_folder, "person icon.png")))
            self.ui.logoutButton.setIcon(QtGui.QIcon(os.path.join(img_folder, "logout.png")))

            self.ui.dashboardButton.setIcon(QtGui.QIcon(os.path.join(img_folder, "paper white.png")))
            self.ui.setupsButton.setIcon(QtGui.QIcon(os.path.join(img_folder, "PC white.png")))
            self.ui.inventoryButton.setIcon(QtGui.QIcon(os.path.join(img_folder, "box.png")))
            self.ui.requestsButton.setIcon(QtGui.QIcon(os.path.join(img_folder, "mail.png")))
            self.ui.registerButton.setIcon(QtGui.QIcon(os.path.join(img_folder, "adduser.png")))
        except Exception:
            pass

        for f in [self.ui.rframe1, self.ui.rframe2, self.ui.rframe4]:
            f.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)

        self.ui.dateEdit.setCalendarPopup(True)
        self.ui.dateEdit.setDate(QtCore.QDate.currentDate())
        self.ui.dateEdit.setDisplayFormat("yyyy-MM-dd")
        self.ui.showAllBox.setChecked(True)
        self.ui.dateEdit.setEnabled(False)

    def setup_tables(self):
        tables = [
            self.ui.assignedComputersTable, self.ui.computerSetupsTable,
            self.ui.issueReportsTable, self.ui.requestReportsTable
        ]
        for table in tables:
            table.verticalHeader().setVisible(False)
            table.horizontalHeader().setStretchLastSection(True)

        self.ui.assignedComputersTable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.ui.assignedComputersTable.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        self.ui.issueReportsTable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.ui.issueReportsTable.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)

    def bind_nav(self, dashboard, setups, inventory, requests, register, logout):
        self.ui.dashboardButton.clicked.connect(dashboard)
        self.ui.setupsButton.clicked.connect(setups)
        self.ui.inventoryButton.clicked.connect(inventory)
        self.ui.requestsButton.clicked.connect(requests)
        self.ui.registerButton.clicked.connect(register)
        self.ui.logoutButton.clicked.connect(logout)

    def bind_dashboard_clicks(self, on_setups, on_logs, on_inv):
        self.ui.rframe1.mousePressEvent = lambda e: on_setups()
        self.ui.rframe2.mousePressEvent = lambda e: on_logs()
        self.ui.rframe4.mousePressEvent = lambda e: on_inv()

    def bind_inventory_actions(self, create_pc, status_report, stock_changes):
        self.ui.createComputerButton.clicked.connect(create_pc)
        self.ui.currentStatusReportButton.clicked.connect(status_report)

        pass

    def bind_stock_buttons(self, callback_factory):
        self.ui.monitorAdd.clicked.connect(callback_factory(0, "Monitor", 1))
        self.ui.pushButton_2.clicked.connect(callback_factory(0, "Monitor", -1))
        self.ui.kmAdd.clicked.connect(callback_factory(1, "Keyboard & Mouse", 1))
        self.ui.kmSub.clicked.connect(callback_factory(1, "Keyboard & Mouse", -1))
        self.ui.gpuAdd.clicked.connect(callback_factory(2, "GPU", 1))
        self.ui.gpuSub.clicked.connect(callback_factory(2, "GPU", -1))
        self.ui.motherboardAdd.clicked.connect(callback_factory(3, "Motherboard", 1))
        self.ui.motherboardSub.clicked.connect(callback_factory(3, "Motherboard", -1))
        self.ui.ramAdd.clicked.connect(callback_factory(4, "RAM", 1))
        self.ui.ramSub.clicked.connect(callback_factory(4, "RAM", -1))

    def bind_request_actions(self, select_req, generate_rep, date_changed, toggle_filter):
        self.ui.selectRequestButton.clicked.connect(select_req)
        self.ui.generateReportButton.clicked.connect(generate_rep)
        self.ui.dateEdit.dateChanged.connect(lambda d: date_changed(d.toString("yyyy-MM-dd")))
        self.ui.showAllBox.toggled.connect(toggle_filter)

    def bind_setup_actions(self, retire_emp):
        self.ui.removeButton.clicked.connect(retire_emp)

    def bind_register_action(self, register_func):
        self.ui.signUpButton.clicked.connect(register_func)

    def switch_page(self, page_name):
        pages = {
            "dashboard": self.ui.dashboard,
            "setups": self.ui.setupFrame,
            "inventory": self.ui.invFrame,
            "requests": self.ui.reqFrame,
            "register": self.ui.registrationFrame
        }
        if page_name in pages:
            self.ui.stackedWidget.setCurrentWidget(pages[page_name])

    def update_generic_table(self, table_name, data, col_indices=None):
        widget = None
        if table_name == "assigned":
            widget = self.ui.assignedComputersTable
        elif table_name == "computers":
            widget = self.ui.computerSetupsTable
        elif table_name == "active_req":
            widget = self.ui.issueReportsTable
        elif table_name == "history_req":
            widget = self.ui.requestReportsTable

        if not widget: return

        widget.setRowCount(0)
        for r, row_data in enumerate(data):
            widget.insertRow(r)
            vals = [row_data[i] for i in col_indices] if col_indices else row_data
            for c, val in enumerate(vals):
                item = QtWidgets.QTableWidgetItem(str(val))
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                widget.setItem(r, c, item)

    def update_hardware_table(self, data):
        table = self.ui.hardwareTable
        table.setRowCount(0)
        for r, row_data in enumerate(data):
            table.insertRow(r)
            header = QtWidgets.QTableWidgetItem(str(row_data[0]))
            table.setVerticalHeaderItem(r, header)

            brand = QtWidgets.QTableWidgetItem(str(row_data[1]))
            brand.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            table.setItem(r, 0, brand)

            qty = QtWidgets.QTableWidgetItem(str(row_data[2]))
            qty.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            table.setItem(r, 1, qty)

    def update_kpi(self, active, items, available):
        self.ui.r1No.setText(str(active))
        self.ui.r2No.setText(str(items))
        self.ui.r2No_3.setText(str(available))

    def get_hardware_qty_at_row(self, row):
        item = self.ui.hardwareTable.item(row, 1)
        return int(item.text()) if item else 0

    def get_selected_setup_id(self):
        row = self.ui.assignedComputersTable.currentRow()
        if row < 0: return None, None
        return self.ui.assignedComputersTable.item(row, 0).text(), self.ui.assignedComputersTable.item(row, 2).text()

    def get_selected_request_row_index(self):
        return self.ui.issueReportsTable.currentRow()

    def get_registration_inputs(self):
        return (self.ui.FNInput.text(), self.ui.MNInput.text(),
                self.ui.LNInput.text(), self.ui.passRegInput.text())

    def clear_registration_inputs(self):
        self.ui.FNInput.clear()
        self.ui.MNInput.clear()
        self.ui.LNInput.clear()
        self.ui.passRegInput.clear()

    def toggle_date_edit(self, enabled):
        self.ui.dateEdit.setEnabled(enabled)

    def get_date_filter_value(self):
        return self.ui.dateEdit.date().toPyDate()

    def is_show_all_checked(self):
        return self.ui.showAllBox.isChecked()

    def show_alert(self, title, msg, type="info"):
        if type == "error":
            QtWidgets.QMessageBox.critical(self, title, msg)
        elif type == "warning":
            QtWidgets.QMessageBox.warning(self, title, msg)
        else:
            QtWidgets.QMessageBox.information(self, title, msg)

    def ask_confirm(self, title, msg):
        reply = QtWidgets.QMessageBox.question(
            self, title, msg,
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No
        )
        return reply == QtWidgets.QMessageBox.StandardButton.Yes

    def open_save_dialog(self, default_name):
        path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save PDF", default_name, "PDF (*.pdf)")
        return path

    def close_view(self):
        self.close()

    def show_view(self):
        self.show()

    def init_graph(self):
        if not HAS_MATPLOTLIB: return
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvasQTAgg(self.figure)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.canvas)
        self.ui.graphWidget.setLayout(layout)

    def draw_graph(self, names, qtys):
        if not HAS_MATPLOTLIB: return
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        colors = []
        for q in qtys:
            if q < 5:
                colors.append('#d32f2f')
            elif q < 10:
                colors.append('#fbc02d')
            else:
                colors.append('#388e3c')

        ax.bar(names, qtys, color=colors)
        plt.setp(ax.get_xticklabels(), rotation=15, ha="right")
        self.figure.tight_layout()
        self.canvas.draw()