import os
from PyQt6 import QtWidgets, QtGui, QtCore
from datetime import datetime

try:
    from fpdf import FPDF

    HAS_FPDF = True
except ImportError:
    HAS_FPDF = False

try:
    from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
    from matplotlib.figure import Figure
    import matplotlib.pyplot as plt

    HAS_MATPLOTLIB = True
except ImportError:
    print("WARNING: Matplotlib not installed. Graphs will be disabled.")
    HAS_MATPLOTLIB = False

from views.ui_Admin import Ui_MainWindow as UiAdmin
from models.admin import AdminModel
from controllers.items_added_controller import ItemsAddedController


class AdminController:
    def __init__(self, admin_id, admin_name):
        self.admin_id = admin_id
        self.admin_name = admin_name

        self.view = QtWidgets.QMainWindow()
        self.ui = UiAdmin()
        self.ui.setupUi(self.view)

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        img_folder = os.path.join(base_dir, "Images")

        try:
            self.ui.label.setPixmap(QtGui.QPixmap(os.path.join(img_folder, "Untitled design (2).png")))
            self.ui.personIcon.setPixmap(QtGui.QPixmap(os.path.join(img_folder, "person icon.png")))
            self.ui.logoutButton.setIcon(QtGui.QIcon(os.path.join(img_folder, "logout.png")))
            self.ui.recordsButton.setIcon(QtGui.QIcon(os.path.join(img_folder, "paper white.png")))
            self.ui.inventoryButton.setIcon(QtGui.QIcon(os.path.join(img_folder, "box.png")))
            self.ui.requestsButton.setIcon(QtGui.QIcon(os.path.join(img_folder, "mail.png")))
            self.ui.inventoryButton_2.setIcon(QtGui.QIcon(os.path.join(img_folder, "PC white.png")))
        except Exception as e:
            print(f"Image load warning: {e}")

        self.ui.label_3.setText(f"Manager: {self.admin_name}")
        self.ui.setupTableWidget.verticalHeader().setVisible(False)
        self.ui.computertableWidget.verticalHeader().setVisible(False)
        self.ui.requesttableWidget.verticalHeader().setVisible(False)
        self.ui.tableWidget.verticalHeader().setVisible(False)

        self.ui.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.ui.setupTableWidget.horizontalHeader().setStretchLastSection(True)
        self.ui.computertableWidget.horizontalHeader().setStretchLastSection(True)

        self.ui.recordsButton.clicked.connect(self.show_dashboard)
        self.ui.inventoryButton_2.clicked.connect(self.show_setups)
        self.ui.inventoryButton.clicked.connect(self.show_inventory)
        self.ui.requestsButton.clicked.connect(self.show_requests)
        self.ui.logoutButton.clicked.connect(self.logout)
        self.ui.requestSelectButton.clicked.connect(self.open_request_action)

        self.ui.requestSelectButton_2.clicked.connect(self.generate_request_report)

        self.ui.requestSelectButton_3.clicked.connect(self.add_new_computer)

        self.ui.rframe1.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.ui.rframe1.mousePressEvent = self.open_setups_from_dashboard
        self.ui.rframe2.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.ui.rframe2.mousePressEvent = self.open_items_added_window
        self.ui.rframe4.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.ui.rframe4.mousePressEvent = self.open_inventory_from_dashboard

        self.ui.monitorAdd.clicked.connect(lambda: self.adjust_quantity(0, "Monitor", 1))
        self.ui.pushButton_2.clicked.connect(lambda: self.adjust_quantity(0, "Monitor", -1))
        self.ui.kmAdd.clicked.connect(lambda: self.adjust_quantity(1, "Keyboard & Mouse", 1))
        self.ui.kmSub.clicked.connect(lambda: self.adjust_quantity(1, "Keyboard & Mouse", -1))
        self.ui.gpuAdd.clicked.connect(lambda: self.adjust_quantity(2, "GPU", 1))
        self.ui.gpuSub.clicked.connect(lambda: self.adjust_quantity(2, "GPU", -1))
        self.ui.motherboardAdd.clicked.connect(lambda: self.adjust_quantity(3, "Motherboard", 1))
        self.ui.motherboardSub.clicked.connect(lambda: self.adjust_quantity(3, "Motherboard", -1))
        self.ui.ramAdd.clicked.connect(lambda: self.adjust_quantity(4, "RAM", 1))
        self.ui.ramSub.clicked.connect(lambda: self.adjust_quantity(4, "RAM", -1))

        try:
            self.load_setup_table()
            self.load_computer_inventory()
            self.load_request_table()
            self.load_request_history()
            self.load_hardware_table()
            self.load_dashboard_kpis()
        except Exception as e:
            print(f"Error loading initial data: {e}")

        self.init_graph()

    def add_new_computer(self):
        reply = QtWidgets.QMessageBox.question(
            self.view, 'Confirm Action',
            "Create a new computer? This will deduct 1 unit from Monitor, K&M, GPU, Mobo, and RAM.",
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No
        )

        if reply == QtWidgets.QMessageBox.StandardButton.Yes:
            try:
                success, message = AdminModel.create_new_computer(self.admin_id)
                if success:
                    QtWidgets.QMessageBox.information(self.view, "Success", message)
                    self.load_computer_inventory()
                    self.load_hardware_table()
                    self.load_dashboard_kpis()
                    self.update_graph()
                else:
                    QtWidgets.QMessageBox.warning(self.view, "Failed", message)
            except Exception as e:
                QtWidgets.QMessageBox.critical(self.view, "System Error", f"Error: {e}")

    def generate_request_report(self):
        if not HAS_FPDF:
            QtWidgets.QMessageBox.critical(self.view, "Error", "PDF Library not installed.")
            return

        row_count = self.ui.tableWidget.rowCount()
        if row_count == 0:
            QtWidgets.QMessageBox.warning(self.view, "Empty", "No records to export.")
            return

        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self.view, "Save Report", f"Request_Records_{datetime.now().strftime('%Y%m%d')}.pdf", "PDF Files (*.pdf)"
        )

        if not file_path: return

        try:
            pdf = FPDF(orientation='L', unit='mm', format='A4')
            pdf.add_page()
            pdf.set_font("Arial", 'B', 16)
            pdf.set_text_color(44, 10, 113)
            pdf.cell(0, 10, "OWLVENTORY - REQUEST HISTORY REPORT", ln=True, align='C')
            pdf.set_font("Arial", '', 10)
            pdf.set_text_color(0, 0, 0)
            pdf.cell(0, 7, f"Admin: {self.admin_name} | Date: {datetime.now().strftime('%Y-%m-%d')}", ln=True,
                     align='C')
            pdf.ln(10)

            columns = ["PC No.", "Emp ID", "Employee Name", "Request", "Action", "Date", "Validator"]
            widths = [15, 25, 45, 45, 30, 55, 55]

            pdf.set_fill_color(65, 35, 127)
            pdf.set_text_color(255, 255, 255)
            pdf.set_font("Arial", 'B', 10)

            for i in range(len(columns)):
                pdf.cell(widths[i], 10, columns[i], border=1, align='C', fill=True)
            pdf.ln()

            pdf.set_text_color(0, 0, 0)
            pdf.set_font("Arial", '', 9)

            for row in range(row_count):
                for col in range(len(columns)):
                    item = self.ui.tableWidget.item(row, col)
                    val = item.text() if item else ""
                    if len(val) > 28: val = val[:25] + "..."
                    pdf.cell(widths[col], 8, val, border=1, align='C')
                pdf.ln()

            pdf.output(file_path)
            QtWidgets.QMessageBox.information(self.view, "Success", "Report Saved.")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self.view, "Error", f"Failed: {e}")

    def open_items_added_window(self, event):
        try:
            self.items_window = ItemsAddedController()
            self.items_window.exec()
        except Exception as e:
            print(f"Error: {e}")

    def adjust_quantity(self, row, hardware_name, amount):
        try:
            current_item = self.ui.hardwaretableWidget.item(row, 1)
            current_val = int(current_item.text()) if current_item else 0

            if current_val + amount < 0:
                QtWidgets.QMessageBox.warning(self.view, "Stock Error",
                                              f"Cannot remove {hardware_name}. Stock is already at 0.")
                return

            AdminModel.update_hardware_stock(hardware_name, amount, self.admin_id)

            # 4. Refresh UI
            self.load_hardware_table()
            self.load_dashboard_kpis()
            self.update_graph()

            if amount > 0:
                QtWidgets.QMessageBox.information(self.view, "Item Added",
                                                  f"Successfully added 1 unit of {hardware_name}.")
            else:
                QtWidgets.QMessageBox.information(self.view, "Item Removed",
                                                  f"Successfully removed 1 unit of {hardware_name}.")

        except Exception as e:
            print(f"Update error: {e}")
            QtWidgets.QMessageBox.critical(self.view, "Error", f"An error occurred: {e}")

    def show_dashboard(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.dashboard)
        self.load_dashboard_kpis()
        self.update_graph()

    def load_dashboard_kpis(self):
        try:
            stats = AdminModel.get_dashboard_kpis()
            self.ui.r1No.setText(str(stats['active_setups']))
            self.ui.r2No.setText(str(stats['total_items']))
            self.ui.r2No_3.setText(str(stats['available_pcs']))
        except Exception as e:
            print(f"KPI Error: {e}")

    def init_graph(self):
        if not HAS_MATPLOTLIB: return
        if not self.ui.graphWidget.layout():
            self.ui.graphWidget.setLayout(QtWidgets.QVBoxLayout())
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.ui.graphWidget.layout().addWidget(self.canvas)
        self.update_graph()

    def update_graph(self):
        if not HAS_MATPLOTLIB: return
        try:
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            data = AdminModel.get_graph_data()
            if data:
                names = [row[0] for row in data]
                quantities = [row[1] for row in data]
                ax.bar(names, quantities, color='#41237F')
                plt.setp(ax.get_xticklabels(), rotation=15, ha="right")
                self.figure.tight_layout()
            self.canvas.draw()
        except Exception as e:
            print(f"Graph Error: {e}")

    def open_setups_from_dashboard(self, event):
        self.show_setups()

    def open_inventory_from_dashboard(self, event):
        self.show_inventory()

    def show_requests(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.reqFrame)
        self.load_request_table()
        self.load_request_history()

    def show_setups(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.setupFrame)
        self.load_setup_table()

    def show_inventory(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.invFrame)
        self.load_computer_inventory()
        self.load_hardware_table()

    def load_request_table(self):
        try:
            data = AdminModel.get_all_requests()
            self.ui.requesttableWidget.setRowCount(0)
            for r_idx, r_data in enumerate(data):
                self.ui.requesttableWidget.insertRow(r_idx)
                for c_idx, d_idx in enumerate([0, 1, 3, 4]):
                    item = QtWidgets.QTableWidgetItem(str(r_data[d_idx]))
                    item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    self.ui.requesttableWidget.setItem(r_idx, c_idx, item)
        except Exception as e:
            print(f"Request error: {e}")

    def load_request_history(self):
        try:
            history = AdminModel.get_request_history()
            self.ui.tableWidget.setRowCount(0)
            for r_idx, r_data in enumerate(history):
                self.ui.tableWidget.insertRow(r_idx)
                for c_idx, value in enumerate(r_data):
                    item = QtWidgets.QTableWidgetItem(str(value))
                    item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    self.ui.tableWidget.setItem(r_idx, c_idx, item)
        except Exception as e:
            print(f"History error: {e}")

    def load_hardware_table(self):
        try:
            inventory = AdminModel.get_hardware_inventory()
            self.ui.hardwaretableWidget.setRowCount(len(inventory))
            for row_idx, data in enumerate(inventory):
                for col_idx, val in enumerate(data):
                    item = QtWidgets.QTableWidgetItem(str(val))
                    item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    self.ui.hardwaretableWidget.setItem(row_idx, col_idx, item)
        except Exception as e:
            print(f"Hardware error: {e}")

    def load_setup_table(self):
        try:
            setups = AdminModel.get_all_setups()
            self.ui.setupTableWidget.setRowCount(0)
            for r, row in enumerate(setups):
                self.ui.setupTableWidget.insertRow(r)
                for c, val in enumerate(row):
                    item = QtWidgets.QTableWidgetItem(str(val))
                    item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    self.ui.setupTableWidget.setItem(r, c, item)
        except Exception as e:
            print(f"Setup error: {e}")

    def load_computer_inventory(self):
        try:
            computers = AdminModel.get_all_computers()
            self.ui.computertableWidget.setRowCount(0)
            for row_idx, row_data in enumerate(computers):
                self.ui.computertableWidget.insertRow(row_idx)
                for col_idx, value in enumerate(row_data):
                    item = QtWidgets.QTableWidgetItem(str(value))
                    item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    self.ui.computertableWidget.setItem(row_idx, col_idx, item)
        except Exception as e:
            print(f"Inventory error: {e}")

    def open_request_action(self):
        row = self.ui.requesttableWidget.currentRow()
        if row < 0: return
        try:
            requests = AdminModel.get_all_requests()
            selected_request = requests[row]
            from controllers.req_action_controller import ReqActionController
            self.action_win = ReqActionController(self.view, selected_request, self.admin_id)
            if self.action_win.exec():
                self.load_request_table()
                self.load_request_history()
                self.load_dashboard_kpis()
        except Exception as e:
            print(f"Error: {e}")

    def logout(self):
        from controllers.login_controller import LoginController
        self.login_controller = LoginController()
        self.login_controller.view.show()
        self.view.close()