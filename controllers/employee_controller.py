import os
from PyQt6 import QtWidgets, QtGui
from views.ui_Employee import Ui_MainWindow as UiEmployee
from models.computer import ComputerModel


class EmployeeController:
    def __init__(self, emp_id, emp_name):
        self.emp_id = emp_id
        self.emp_name = emp_name

        self.view = QtWidgets.QMainWindow()
        self.ui = UiEmployee()
        self.ui.setupUi(self.view)

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        img_folder = os.path.join(base_dir, "Images")

        self.ui.label.setPixmap(QtGui.QPixmap(os.path.join(img_folder, "Untitled design (2).png")))
        self.ui.personIcon.setPixmap(QtGui.QPixmap(os.path.join(img_folder, "person icon.png")))
        self.ui.label_5.setPixmap(QtGui.QPixmap(os.path.join(img_folder, "pc logo white.png")))
        self.ui.label_7.setPixmap(QtGui.QPixmap(os.path.join(img_folder, "pc pic (1000 x 1000 px).png")))

        logout_icon = QtGui.QIcon()
        logout_icon.addPixmap(QtGui.QPixmap(os.path.join(img_folder, "logout.png")))
        self.ui.logoutButton.setIcon(logout_icon)

        self.ui.label_3.setText(f"Employee ID: {self.emp_id}")

        self.assign_or_show_pc()

        self.ui.logoutButton.clicked.connect(self.logout)
        self.ui.pushButton.clicked.connect(self.open_request_form)

    def open_request_form(self):
        from controllers.request_controller import RequestController
        self.request_form = RequestController(self.view)
        self.request_form.show()

    def assign_or_show_pc(self):
        try:
            pc = ComputerModel.get_pc_by_employee(self.emp_id)
            if pc:
                self.ui.label_6.setText(f"PC #{pc[0]}")
            else:
                pc_number = ComputerModel.assign_pc(self.emp_id)
                if pc_number:
                    self.ui.label_6.setText(f"PC #{pc_number}")
                else:
                    self.ui.label_6.setText("No PC Available")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self.view, "Error", f"Database error: {e}")

    def open_request_form(self):
        from controllers.request_controller import RequestController
        from models.computer import ComputerModel

        pc_data = ComputerModel.get_pc_by_employee(self.emp_id)

        if pc_data:
            pc_no = pc_data[0]  # pcNo attribute
            self.request_form = RequestController(self.view, self.emp_id, pc_no)
            self.request_form.show()
        else:
            QtWidgets.QMessageBox.warning(self.view, "Error", "No assigned PC found for your account.")

    def logout(self):
        from controllers.login_controller import LoginController
        self.login_controller = LoginController()
        self.login_controller.view.show()
        self.view.close()